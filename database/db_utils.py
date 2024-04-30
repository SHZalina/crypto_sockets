import psycopg2
import os
import sys
sys.path.append(os.getcwd())
 
from configs.db_config import *
 
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
 
 
def check_user_in_db(login: str) -> bool:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT EXISTS (SELECT 1 FROM users WHERE login = '{login}');""")
            return cursor.fetchone()[0]
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
 
def return_w(login: str) -> str:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT w FROM users WHERE login = '{login}';""")
            return cursor.fetchone()[0]
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
 
def return_password(login: str) -> str:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT password FROM users WHERE login = '{login}';""")
            return cursor.fetchone()[0]
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
 
def insert_user_data(login: str, password: str) -> int:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO users (login, password) VALUES
            ('{login}', '{password}')
            RETURNING id;""")
            connection.commit()
            return cursor.fetchone()[0]
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
 
def insert_rsa_data(id: int, p: int, q: int, n: int, phi: int, e: int, d: int) -> None:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO RSA (user_id, p, q, n, phi, e, d)
            VALUES ({id}, {p}, {q}, {n}, {phi}, {e}, {d});""")
            connection.commit()
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
 
def insert_user_time(login: str, time) -> None:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE Users
            SET t = '{time}'
            WHERE login = '{login}';""")
            connection.commit()
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
 
def insert_user_w(login: str, slovo: str) -> None:
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE Users
            SET w = '{slovo}'
            WHERE login = '{login}';""")
            connection.commit()
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()

def get_time(login: str):
    try:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT t
            FROM Users
            WHERE login = '{login}';
""")
            return cursor.fetchone()[0]
    except Exception as exc:
        print(exc)
    finally:
        if connection:
            connection.close()
# insert_user_data(1, 1, 1, '12.01.23')
# print(check_user_in_db('2'))
# print(return_w ('privet'))