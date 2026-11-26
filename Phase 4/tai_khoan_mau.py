"""Show coursework sample website accounts to the local project owner."""
import sys
from mysql.connector import Error
from app import connect
from kiem_tra_database import friendly_error

try:
    conn = connect()
    try:
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute('''SELECT u.username,u.password FROM users u
                WHERE EXISTS (SELECT 1 FROM profile p WHERE p.user_id=u.user_id)
                  AND EXISTS (SELECT 1 FROM subscription s
                    WHERE s.user_id=u.user_id AND s.status='ACTIVE'
                      AND s.start_date<=CURDATE()
                      AND (s.end_date IS NULL OR s.end_date>=CURDATE()))
                ORDER BY u.user_id LIMIT 5''')
            rows = cur.fetchall()
        finally:
            cur.close()
    finally:
        conn.close()
    print('TAI KHOAN WEBSITE MAU TRONG DU LIEU BAI TAP')
    print('Day la tai khoan website, khac voi tai khoan root MySQL.\n')
    for row in rows:
        print('Username:', row['username'])
        print('Password:', row['password'])
        print()
    if not rows:
        print('Chua co tai khoan voi profile va goi ACTIVE con hieu luc.')
except (Error, KeyError, ValueError, RuntimeError) as err:
    print(friendly_error(err))
    sys.exit(1)
