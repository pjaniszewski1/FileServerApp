import re
import os
import psycopg2
from psycopg2.extras import DictCursor
import psycopg2.sql as sql
from contextlib import closing
from datetime import datetime, timedelta
from aiohttp import web
from uuid import uuid4
from server.crypto import HashAPI

EMAIL_REGEX = re.compile(r'[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}$')
PASSWORD_REGEX = re.compile(f'^\w{8,50}$')

conn_params = {
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST']
}

dt_format = os.environ['DATE_FORMAT']

class UsersSQLAPI:
    @staticmethod
    def authorized(func):
        def wrapper(*args, **kwargs) -> web.Response:
            request = args[1]
            session_id = request.headers.get('X-Authorization')

            if not session_id:
                raise web.HTTPUnauthorized(text='Unauthorized request')

            with closing(psycopg2.connect(**conn_params)) as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(sql.SQL('SELECT * FROM public."Sessions" WHERE "UUID" = {}').format(
                        sql.Literal(session_id)
                    ))

                    session = cursor.fetchone()

                    if not session:
                        raise web.HTTPUnauthorized(text='Session expired. Please, sign in again')

                    if session['ExpirationDate'] < datetime.now():
                        cursor.execute(
                            sql.SQL('DELETE FROM public."Sessions" WHERE "id" = {}').format(sql.Literal(session['id']))
                        )
                        raise web.HTTPUnauthorized(text='Session expired. Please, sign in again')

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def signup(**kwargs):

        email = kwargs.get('email')
        password = kwargs.get('password')
        confirm_password = kwargs.get('confirm_password')
        name = kwargs.get('name')
        surname = kwargs.get('surname')

        assert email and (email := email.strip()), 'Email is not set'
        assert password and (password := password.strip()), 'Password is not set'
        assert confirm_password and (confirm_password := confirm_password.strip()), 'Please, repeat the password'
        assert name and (name := name.strip()), 'Name is not set'

        assert EMAIL_REGEX.match(email), 'Invalid email format'
        assert PASSWORD_REGEX.match(password),\
            'Invalid password. Password should contain letters, digits and will be 8 to 50 characters long'
        assert password == confirm_password, 'Passwords are not match'

        if surname:
            surname = surname.strip()

        hashed_password = HashAPI.hash_sha512(password)

        with closing(psycopg2.connect(**conn_params)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql.SQL('SELECT * FROM public."User" WHERE "Email" = {}').format(sql.Literal(email)))
                existed_user = cursor.fetchone()
                assert not existed_user, 'User with email {} already exists'.format(email)

                columns = ('CreatedDate', 'EMail', 'Password', 'Name', 'Surname')
                values = (datetime.strftime(datetime.now(), dt_format), email, hashed_password, name, surname)

                cursor.execute(sql.SQL(
                    'INSERT INTO public."User" ({}) VALUES ({})').format(
                    sql.SQL(', '.join(map(sql.Identifier, columns))),
                    sql.SQL(', '.join(map(sql.Literal, values)))
                ))

                conn.commit()

    @staticmethod
    def logout(session_id: str):
        with closing(psycopg2.connect(**conn_params)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(sql.SQL('DELETE FROM public."Session" WHERE "UUID" = {}').format(
                    sql.Literal(session_id)
                ))
                conn.commit()












