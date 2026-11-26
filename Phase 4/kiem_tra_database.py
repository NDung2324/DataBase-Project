"""Check the configured coursework database without changing its data."""
from pathlib import Path
import sys

from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv(Path(__file__).with_name('.env'))

TABLES = ('users', 'profile', 'content', 'movies', 'episode', 'tv_series',
          'subscription', 'subscription_plan', 'watch_history')
TRIGGERS = {'trg_validate_watch_duration', 'trg_validate_profile_limit'}


def check_database(verbose=True):
    from app import connect
    conn = connect()
    try:
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute('SELECT DATABASE() AS db_name, VERSION() AS version')
            result = cur.fetchone()
            cur.execute("SELECT TABLE_NAME AS name FROM information_schema.TABLES "
                        "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_TYPE='BASE TABLE'")
            present = {row['name'].lower() for row in cur.fetchall()}
            missing = set(TABLES) - present
            if missing:
                raise RuntimeError('Database thieu bang: ' + ', '.join(sorted(missing)))
            result['counts'] = {}
            for table in TABLES:
                cur.execute('SELECT COUNT(*) AS n FROM `' + table + '`')
                result['counts'][table] = cur.fetchone()['n']
            cur.execute('SELECT TRIGGER_NAME AS name FROM information_schema.TRIGGERS '
                        'WHERE TRIGGER_SCHEMA=DATABASE()')
            result['triggers'] = [row['name'] for row in cur.fetchall()]
            result['missing_triggers'] = sorted(TRIGGERS - set(result['triggers']))
        finally:
            cur.close()
    finally:
        conn.close()
    if verbose:
        print('KET NOI MYSQL THANH CONG')
        print('Database:', result['db_name'], '| MySQL:', result['version'])
        for name, count in result['counts'].items():
            print('  %-20s %s' % (name, count))
        if result['missing_triggers']:
            print('CHU Y: thieu trigger:', ', '.join(result['missing_triggers']))
        else:
            print('Hai trigger cua bao cao: da co du.')
    return result


def friendly_error(err):
    number = getattr(err, 'errno', None)
    if number == 1045:
        return ('MySQL tu choi thong tin dang nhap. Mo file .env, sua DB_USER va '
                'DB_PASSWORD theo tai khoan MySQL tren may ban, sau do luu lai.')
    if number == 1049:
        return ('Khong tim thay database. Kiem tra DB_NAME trong .env; '
                'database da kiem thu la mini_netflix_check.')
    if number in (2002, 2003, 2005):
        return ('Chua ket noi duoc MySQL. Kiem tra MySQL Server dang chay, '
                'DB_HOST=127.0.0.1 va DB_PORT=3306 trong .env.')
    if isinstance(err, KeyError):
        return 'File .env chua co DB_NAME. Dat DB_NAME=mini_netflix_check.'
    if isinstance(err, RuntimeError):
        return str(err)
    return 'Khong kiem tra duoc database (ma loi %s). Kiem tra lai cau hinh .env.' % number


if __name__ == '__main__':
    try:
        check_database()
    except (Error, KeyError, ValueError, RuntimeError) as err:
        print(friendly_error(err))
        sys.exit(1)
