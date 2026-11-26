"""Mini-Netflix Phase 4: Flask client demo, uses the original nine MySQL tables.

Demo notes: plaintext passwords are used ONLY to match the supplied coursework data.
The watch player is a simulated timer, not a real video streaming service.
"""
import os
import secrets
from uuid import uuid4
from datetime import datetime
from contextlib import contextmanager
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
import mysql.connector
from mysql.connector import Error
from itsdangerous import URLSafeSerializer, BadSignature

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'local-demo-only-change-this')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')


def connect():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.environ['DB_NAME'],
        connection_timeout=5,
        charset='utf8mb4',
    )


@contextmanager
def db_cursor():
    conn = connect()
    cur = conn.cursor(dictionary=True)
    try:
        yield cur
    finally:
        cur.close()
        conn.close()


def select_all(sql, params=()):
    with db_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def select_one(sql, params=()):
    with db_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute_write(sql, params):
    conn = connect()
    try:
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
    finally:
        conn.close()


def csrf_token():
    if '_csrf' not in session:
        session['_csrf'] = secrets.token_hex(24)
    return session['_csrf']


app.jinja_env.globals['csrf_token'] = csrf_token


def valid_csrf():
    provided = request.form.get('_csrf', '')
    stored = session.get('_csrf', '')
    return bool(provided and stored and secrets.compare_digest(provided, stored))


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def active_plan(user_id, cursor=None):
    sql = '''SELECT s.subscription_id, sp.plan_id, sp.plan_name,
        sp.price, sp.quality, sp.max_profiles, s.start_date, s.end_date
        FROM subscription s JOIN subscription_plan sp ON sp.plan_id=s.plan_id
        WHERE s.user_id=%s AND s.status='ACTIVE'
          AND s.start_date<=CURDATE()
          AND (s.end_date IS NULL OR s.end_date>=CURDATE())
        ORDER BY s.start_date DESC, s.subscription_id DESC LIMIT 1'''
    if cursor is not None:
        cursor.execute(sql, (user_id,))
        return cursor.fetchone()
    return select_one(sql, (user_id,))


def current_viewing(profile_id, content_id):
    # Existing schemas have no viewing timestamp. Prefer unfinished progress;
    # do not let a previous completed playthrough hide an unfinished replay.
    return select_one('''SELECT watch_history_id, watch_duration, completed
        FROM watch_history WHERE profile_id=%s AND content_id=%s
        ORDER BY completed ASC, watch_duration DESC, watch_history_id DESC LIMIT 1''',
        (profile_id, content_id))


def viewing_serializer():
    return URLSafeSerializer(app.secret_key, salt='mini-netflix-viewing')


def insert_owned_profile(profile_id, name, birthdate):
    conn = connect()
    try:
        conn.start_transaction()
        cur = conn.cursor(dictionary=True)
        try:
            # Plan activation locks the same account row. Concurrent profile
            # creations therefore cannot both pass the trigger's count check.
            cur.execute('SELECT user_id FROM users WHERE user_id=%s FOR UPDATE',
                        (session['user_id'],))
            if not cur.fetchone():
                abort(404)
            cur.execute('''INSERT INTO profile(profile_id,user_id,profile_name,birthdate)
                VALUES(%s,%s,%s,%s)''',
                (profile_id, session['user_id'], name, birthdate))
            conn.commit()
        finally:
            cur.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def owned_profile(profile_id):
    return select_one('''SELECT p.profile_id, p.profile_name, p.birthdate,
        p.user_id, u.username FROM profile p JOIN users u ON u.user_id=p.user_id
        WHERE p.profile_id=%s AND p.user_id=%s''',
        (profile_id, session['user_id']))


def selected_profile():
    profile_id = session.get('profile_id')
    return owned_profile(profile_id) if profile_id else None


def db_error_message(err):
    if getattr(err, 'errno', None) == 1644:
        return 'Trigger MySQL từ chối: ' + err.msg
    if getattr(err, 'errno', None) == 1062:
        return 'Mã đã tồn tại. Thử lại.'
    if getattr(err, 'errno', None) == 1452:
        return 'Thông tin tham chiếu (Foreign Key) không tồn tại.'
    return 'MySQL từ chối thao tác: ' + getattr(err, 'msg', str(err))


def new_id(prefix):
    return prefix + uuid4().hex[:14].upper()  # Fits VARCHAR(20)


@app.context_processor
def context_user():
    return {'logged_username': session.get('username'),
            'current_profile_name': session.get('profile_name')}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        if not valid_csrf():
            abort(400, 'CSRF token không hợp lệ.')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Nhập username và password.', 'error')
        else:
            try:
                # Coursework database uses plaintext passwords. Parameterized SQL.
                user = select_one('''SELECT user_id, username FROM users
                    WHERE BINARY username = BINARY %s AND BINARY password = BINARY %s
                    LIMIT 1''', (username, password))
                if user:
                    session.clear()
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['_csrf'] = secrets.token_hex(24)
                    return redirect(url_for('profiles'))
                flash('Sai username hoặc password.', 'error')
            except (Error, KeyError) as err:
                flash(db_error_message(err), 'error')
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    if not valid_csrf():
        abort(400)
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    try:
        profile = selected_profile()
        plan = active_plan(session['user_id'])
        counts = {
            'My Profiles': select_one('SELECT COUNT(*) AS n FROM profile WHERE user_id=%s',
                                     (session['user_id'],))['n'],
            'Movies': select_one('SELECT COUNT(*) AS n FROM movies')['n'],
            'Episodes': select_one('SELECT COUNT(*) AS n FROM episode')['n'],
            'My Views': select_one('''SELECT COUNT(*) AS n FROM watch_history w
                JOIN profile p ON p.profile_id=w.profile_id WHERE p.user_id=%s''',
                (session['user_id'],))['n'],
        }
        popular = select_all('''SELECT c.content_id, c.title, COUNT(w.watch_history_id) AS views
            FROM content c JOIN watch_history w ON c.content_id=w.content_id
            GROUP BY c.content_id, c.title ORDER BY views DESC, c.content_id LIMIT 8''')
        return render_template('home.html', counts=counts, popular=popular,
                               profile=profile, plan=plan)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/profiles')
@login_required
def profiles():
    keyword = request.args.get('q', '').strip()[:100]
    pattern = f'%{keyword}%'
    try:
        rows = select_all('''SELECT p.profile_id,p.profile_name,p.birthdate,
            (SELECT COUNT(*) FROM watch_history w WHERE w.profile_id=p.profile_id) AS total_views
            FROM profile p WHERE p.user_id=%s
              AND (%s='' OR p.profile_id LIKE %s OR p.profile_name LIKE %s)
            ORDER BY p.profile_name LIMIT 100''',
            (session['user_id'], keyword, pattern, pattern))
        return render_template('profiles.html', profiles=rows, q=keyword,
                               plan=active_plan(session['user_id']),
                               current_id=session.get('profile_id'))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/profiles/select/<profile_id>', methods=['POST'])
@login_required
def select_profile(profile_id):
    if not valid_csrf():
        abort(400)
    try:
        profile = owned_profile(profile_id)
        if not profile:
            abort(404)
        session['profile_id'] = profile['profile_id']
        session['profile_name'] = profile['profile_name']
        flash('Đã chọn Profile: ' + profile['profile_name'], 'success')
        return redirect(url_for('movies'))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/profiles/add', methods=['GET', 'POST'])
@login_required
def add_profile():
    values = {'profile_name': '', 'birthdate': ''}
    if request.method == 'POST':
        if not valid_csrf():
            abort(400)
        values = {key: request.form.get(key, '').strip() for key in values}
        if not values['profile_name'] or len(values['profile_name']) > 20:
            flash('Profile Name bắt buộc, tối đa 20 ký tự.', 'error')
        else:
            try:
                birthdate = values['birthdate'] or None
                if birthdate:
                    datetime.strptime(birthdate, '%Y-%m-%d')
                profile_id = new_id('PR')
                insert_owned_profile(profile_id, values['profile_name'], birthdate)
                flash('Đã tạo Profile thành công!', 'success')
                return redirect(url_for('profiles'))
            except ValueError:
                flash('Ngày sinh không hợp lệ.', 'error')
            except (Error, KeyError) as err:
                flash(db_error_message(err), 'error')
    try:
        return render_template('add_profile.html', values=values,
                               plan=active_plan(session['user_id']))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/profiles/<profile_id>')
@login_required
def profile_detail(profile_id):
    try:
        profile = owned_profile(profile_id)
        if not profile:
            abort(404)
        subs = select_all('''SELECT s.subscription_id,s.status,s.start_date,s.end_date,
            sp.plan_name,sp.price,sp.quality,sp.max_profiles
            FROM subscription s JOIN subscription_plan sp ON sp.plan_id=s.plan_id
            WHERE s.user_id=%s ORDER BY s.start_date DESC,s.subscription_id DESC''',
            (session['user_id'],))
        count = select_one('SELECT COUNT(*) AS n FROM profile WHERE user_id=%s',
                           (session['user_id'],))['n']
        return render_template('profile_detail.html', profile=profile,
                               active=active_plan(session['user_id']),
                               subscriptions=subs, profile_count=count)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/plans')
@login_required
def plans():
    try:
        rows = select_all('''SELECT plan_id,plan_name,price,quality,max_profiles
            FROM subscription_plan ORDER BY price,plan_name''')
        return render_template('plans.html', plans=rows)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/plans/activate/<plan_id>', methods=['POST'])
@login_required
def activate_plan(plan_id):
    # Demo activation: MySQL supplies both dates, one calendar month apart.
    if not valid_csrf():
        abort(400)
    conn = None
    try:
        conn = connect()
        conn.start_transaction()
        cur = conn.cursor(dictionary=True)
        try:
            # Serialize changes by this account, including repeated clicks.
            cur.execute('SELECT user_id FROM users WHERE user_id=%s FOR UPDATE',
                        (session['user_id'],))
            if not cur.fetchone():
                conn.rollback()
                session.clear()
                return redirect(url_for('login'))

            cur.execute('''SELECT plan_id, plan_name, max_profiles
                           FROM subscription_plan WHERE plan_id=%s''', (plan_id,))
            plan = cur.fetchone()
            if not plan:
                conn.rollback()
                abort(404)

            # A downgrade cannot invalidate profiles the user has already created.
            cur.execute('SELECT COUNT(*) AS n FROM profile WHERE user_id=%s',
                        (session['user_id'],))
            count = cur.fetchone()['n']
            if count > plan['max_profiles']:
                conn.rollback()
                flash(f"Không thể chọn {plan['plan_name']}: tài khoản có {count} Profile "
                      f"nhưng gói chỉ cho phép {plan['max_profiles']}.", 'error')
                return redirect(url_for('plans'))

            # Retain history; never allow overlapping ACTIVE subscriptions for this user.
            cur.execute('''UPDATE subscription SET status='CANCELLED'
                           WHERE user_id=%s AND status='ACTIVE' ''',
                        (session['user_id'],))
            subscription_id = new_id('SU')
            cur.execute('''INSERT INTO subscription
                        (subscription_id, user_id, plan_id, status, start_date, end_date)
                        VALUES (%s, %s, %s, 'ACTIVE', CURDATE(),
                                DATE_ADD(CURDATE(), INTERVAL 1 MONTH))''',
                        (subscription_id, session['user_id'], plan_id))
            conn.commit()
            flash(f"Kích hoạt gói {plan['plan_name']} thành công! "
                  "Thời hạn một tháng tính từ hôm nay.", 'success')
            return redirect(url_for('subscriptions'))
        finally:
            cur.close()
    except Error as err:
        if conn:
            conn.rollback()
        flash(db_error_message(err), 'error')
        return redirect(url_for('plans'))
    finally:
        if conn:
            conn.close()


@app.route('/subscriptions')
@login_required
def subscriptions():
    try:
        rows = select_all('''SELECT s.subscription_id,s.user_id,s.plan_id,
            sp.plan_name,sp.price,sp.quality,sp.max_profiles,
            s.status,s.start_date,s.end_date,
            CASE WHEN s.status='ACTIVE' AND s.start_date<=CURDATE()
                AND (s.end_date IS NULL OR s.end_date>=CURDATE())
                THEN 1 ELSE 0 END AS currently_valid
            FROM subscription s JOIN subscription_plan sp ON sp.plan_id=s.plan_id
            WHERE s.user_id=%s ORDER BY s.start_date DESC,s.subscription_id DESC''',
            (session['user_id'],))
        return render_template('subscriptions.html', subscriptions=rows,
                               active=active_plan(session['user_id']))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/movies')
@login_required
def movies():
    keyword = request.args.get('q', '').strip()[:100]
    category = request.args.get('category', '').strip()[:15]
    try:
        categories = select_all('''SELECT DISTINCT category FROM content
            WHERE content_type='MOVIE' AND category IS NOT NULL ORDER BY category''')
        rows = select_all('''SELECT c.content_id,c.title,c.category,c.release_date,
            c.duration,c.description FROM content c JOIN movies m ON c.content_id=m.content_id
            WHERE c.title LIKE %s AND (%s='' OR c.category=%s)
            ORDER BY c.title LIMIT 100''', (f'%{keyword}%', category, category))
        return render_template('movies.html', movies=rows, categories=categories,
                               q=keyword, selected_category=category,
                               has_profile=bool(selected_profile()))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/series')
@login_required
def series():
    try:
        rows = select_all('''SELECT ts.series_id,ts.series_name,
            COUNT(e.content_id) AS episodes FROM tv_series ts
            LEFT JOIN episode e ON e.series_id=ts.series_id
            GROUP BY ts.series_id,ts.series_name ORDER BY ts.series_name''')
        return render_template('series.html', series=rows)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/series/<series_id>')
@login_required
def series_detail(series_id):
    season = request.args.get('season', type=int)
    try:
        series_row = select_one('SELECT series_id,series_name FROM tv_series WHERE series_id=%s',
                                (series_id,))
        if not series_row:
            abort(404)
        seasons = select_all('''SELECT season_number,COUNT(*) AS episode_count
            FROM episode WHERE series_id=%s GROUP BY season_number ORDER BY season_number''',
            (series_id,))
        episodes = select_all('''SELECT e.content_id,e.season_number,e.episode_number,
            c.title,c.duration,c.release_date,c.description
            FROM episode e JOIN content c ON c.content_id=e.content_id
            WHERE e.series_id=%s AND (%s IS NULL OR e.season_number=%s)
            ORDER BY e.season_number,e.episode_number''', (series_id, season, season))
        return render_template('series_detail.html', series=series_row, seasons=seasons,
                               episodes=episodes, selected_season=season,
                               has_profile=bool(selected_profile()))
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/watch/<content_id>')
@login_required
def watch(content_id):
    try:
        profile = selected_profile()
        if not profile:
            flash('Vui lòng chọn Profile trước khi xem.', 'error')
            return redirect(url_for('profiles'))
        plan = active_plan(session['user_id'])
        if not plan:
            flash('Tài khoản chưa có subscription đang hiệu lực. Không thể xem nội dung.', 'error')
            return redirect(url_for('subscriptions'))
        content = select_one('''SELECT content_id,title,duration,content_type,
            description,release_date FROM content WHERE content_id=%s''', (content_id,))
        if not content:
            abort(404)
        # Current progress is scoped to the selected profile and this content.
        progress = current_viewing(profile['profile_id'], content_id)
        restart = request.args.get('restart') == '1'
        resume = bool(progress and not progress['completed'] and not restart)
        start_minutes = min(int(progress['watch_duration']), int(content['duration'])) if resume else 0
        viewing_token = viewing_serializer().dumps({
            'user_id': session['user_id'], 'profile_id': profile['profile_id'],
            'content_id': content_id,
            'watch_history_id': progress['watch_history_id'] if resume else new_id('WH'),
        })
        return render_template('watch.html', content=content, profile=profile, plan=plan,
                               start_minutes=start_minutes, restarting=restart,
                               viewing_token=viewing_token)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/watch/<content_id>/save', methods=['POST'])
@login_required
def save_watch(content_id):
    if not valid_csrf():
        abort(400)
    try:
        profile = selected_profile()
        if not profile:
            flash('Vui lòng chọn Profile.', 'error')
            return redirect(url_for('profiles'))
        if not active_plan(session['user_id']):
            flash('Subscription không còn hiệu lực.', 'error')
            return redirect(url_for('subscriptions'))
        content = select_one('SELECT content_id,duration FROM content WHERE content_id=%s',
                             (content_id,))
        if not content:
            abort(404)
        # Client sends simulated minutes. Validate on the server and let MySQL trigger enforce duration.
        minutes = int(request.form.get('watch_duration', '-1'))
        if minutes < 0 or minutes > content['duration']:
            flash('Thời gian xem phải trong khoảng 0 đến thời lượng nội dung.', 'error')
            return redirect(url_for('watch', content_id=content_id))
        completed = int(minutes >= content['duration'])
        try:
            viewing = viewing_serializer().loads(request.form.get('viewing_token', ''))
        except BadSignature:
            abort(400, 'Trang xem không còn hợp lệ. Hãy mở lại nội dung.')
        if not isinstance(viewing, dict) or viewing.get('user_id') != session['user_id'] or viewing.get('content_id') != content_id:
            abort(400)
        if viewing.get('profile_id') != profile['profile_id']:
            flash('Profile đã thay đổi ở tab khác. Chọn lại profile và mở lại nội dung trước khi lưu.', 'error')
            return redirect(url_for('profiles'))
        history_id = viewing.get('watch_history_id')
        if not isinstance(history_id, str) or not history_id or len(history_id) > 20:
            abort(400)
        conn = connect()
        try:
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)
            try:
                cur.execute('SELECT user_id FROM users WHERE user_id=%s FOR UPDATE',
                            (session['user_id'],))
                if not cur.fetchone():
                    abort(404)
                cur.execute('SELECT profile_id FROM profile WHERE profile_id=%s AND user_id=%s',
                            (profile['profile_id'], session['user_id']))
                if not cur.fetchone():
                    abort(404)
                if not active_plan(session['user_id'], cursor=cur):
                    flash('Subscription không còn hiệu lực.', 'error')
                    return redirect(url_for('subscriptions'))
                cur.execute('SELECT duration FROM content WHERE content_id=%s', (content_id,))
                current_content = cur.fetchone()
                if not current_content:
                    abort(404)
                if minutes > current_content['duration']:
                    flash('Thời lượng nội dung đã thay đổi. Hãy mở lại nội dung.', 'error')
                    return redirect(url_for('watch', content_id=content_id))
                cur.execute('''SELECT profile_id,content_id,watch_duration FROM watch_history
                    WHERE watch_history_id=%s FOR UPDATE''', (history_id,))
                existing = cur.fetchone()
                if existing:
                    if existing['profile_id'] != profile['profile_id'] or existing['content_id'] != content_id:
                        abort(400)
                    minutes = max(minutes, int(existing['watch_duration']))
                    if minutes > current_content['duration']:
                        flash('Tiến độ cũ vượt thời lượng hiện tại. Hãy mở lại nội dung.', 'error')
                        return redirect(url_for('watch', content_id=content_id))
                    completed = int(minutes >= current_content['duration'])
                    cur.execute('''UPDATE watch_history SET watch_duration=%s,completed=%s
                        WHERE watch_history_id=%s AND profile_id=%s''',
                        (minutes, completed, history_id, profile['profile_id']))
                else:
                    completed = int(minutes >= current_content['duration'])
                    cur.execute('''INSERT INTO watch_history
                        (watch_history_id,profile_id,content_id,watch_duration,completed)
                        VALUES(%s,%s,%s,%s,%s)''',
                        (history_id, profile['profile_id'], content_id, minutes, completed))
                conn.commit()
            finally:
                cur.close()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        flash(f'Đã lưu tiến độ {minutes}/{content["duration"]} phút cho Profile '
              f'{profile["profile_name"]} vào MySQL!', 'success')
        return redirect(url_for('history'))
    except (TypeError, ValueError):
        flash('Dữ liệu thời gian xem không hợp lệ.', 'error')
        return redirect(url_for('watch', content_id=content_id))
    except (Error, KeyError) as err:
        flash(db_error_message(err), 'error')
        return redirect(url_for('watch', content_id=content_id))


@app.route('/history')
@login_required
def history():
    try:
        profile = selected_profile()
        if not profile:
            flash('Chọn Profile để xem lịch sử.', 'error')
            return redirect(url_for('profiles'))
        # Use the same unfinished-first rule as the player, even after a replay.
        rows = select_all('''SELECT c.content_id,c.title,c.duration,
            w.watch_duration,w.completed,w.sessions
            FROM (
                SELECT h.*, COUNT(*) OVER (PARTITION BY h.content_id) AS sessions,
                    ROW_NUMBER() OVER (PARTITION BY h.content_id
                        ORDER BY h.completed ASC,h.watch_duration DESC,h.watch_history_id DESC) AS position
                FROM watch_history h JOIN profile p ON p.profile_id=h.profile_id
                WHERE p.user_id=%s AND p.profile_id=%s
            ) w JOIN content c ON c.content_id=w.content_id
            WHERE w.position=1 ORDER BY c.title,c.content_id LIMIT 100''',
            (session['user_id'], profile['profile_id']))
        return render_template('history.html', history=rows, profile=profile)
    except (Error, KeyError) as err:
        return render_template('error.html', message=str(err)), 500


@app.route('/history/add')
@login_required
def add_watch_history():
    # No manual watch history input in the client website.
    return redirect(url_for('movies'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
