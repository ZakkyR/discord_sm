import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


def upsert_server_mst(server_id: int, lang: str = 'J', pin_mode: str = '0', all_mention: bool = False):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:

            if count_server_mst(server_id) > 0:
                cur.execute(
                    "UPDATE MST_SERVER SET LANG = %s, PIN_MODE = %s, ALL_MENTION = %s WHERE SERVER_ID = %s;",
                    (lang, pin_mode, _bool2str(all_mention), str(server_id))
                )
            else:
                cur.execute(
                    "INSERT INTO MST_SERVER (SERVER_ID, LANG, PIN_MODE, ALL_MENTION) VALUES (%s, %s, %s, %s);",
                    (str(server_id), lang, pin_mode, _bool2str(all_mention))
                )

            conn.commit()


def count_server_mst(server_id: int):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM MST_SERVER WHERE SERVER_ID = %s;",
                (str(server_id),)
            )

            count = cur.fetchone()[0]

            return count


def insert_user_mst(server_id: int, user_id: int):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO MST_USER (SERVER_ID, USER_ID) VALUES (%s, %s);",
                (str(server_id), str(user_id))
            )

            conn.commit()


def count_user_mst(server_id: int, user_id: int):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM MST_USER WHERE SERVER_ID = %s AND USER_ID = %s;",
                (str(server_id), str(user_id))
            )

            count = cur.fetchone()[0]

            return count


def delete_user_mst(server_id: int, user_id: int):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM MST_USER WHERE SERVER_ID = %s AND USER_ID = %s;",
                (str(server_id), str(user_id))
            )

            conn.commit()


def insert_shortcut(server_id: int, shortcut: str, message: str):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO MST_MESSAGE_SHORTCUT (SERVER_ID, SC_KEY, MESSAGE) VALUES (%s, %s, %s);",
                (str(server_id), shortcut, message)
            )

            conn.commit()


def get_shortcut_message(server_id: int, shortcut: str):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT MESSAGE FROM MST_MESSAGE_SHORTCUT WHERE SERVER_ID = %s AND SC_KEY = %s;",
                (str(server_id), shortcut)
            )

            rows = cur.fetchall()

            res = None

            if len(rows) > 0:
                res = rows[0][0]

            return res


def delete_shortcut(server_id: int, shortcut: str):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM MST_MESSAGE_SHORTCUT WHERE SERVER_ID = %s AND SC_KEY = %s;",
                (str(server_id), shortcut)
            )

            conn.commit()


def get_shortcut_list(server_id: int):
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT SC_KEY FROM MST_MESSAGE_SHORTCUT WHERE SERVER_ID = %s;",
                (str(server_id),)
            )

            rows = cur.fetchall()

            return rows


# Tool
def _bool2str(b: bool):
    return 'X' if b else 'A'
