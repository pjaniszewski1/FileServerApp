import psycopg2
import psycopg2.sql as sql
import os
from datetime import datetime

dt_format = os.environ['DATE_FORMAT']


class DataBase:
    def __init__(self) -> None:
        pass

    def init_system(self) -> None:
        print('init database...')
        try:
            conf = {
                'database': os.environ['DB_NAME'],
                'user': os.environ['DB_USER'],
                'password': os.environ['DB_PASSWORD'],
                'host': os.environ['DB_HOST'],
                'port': 5432
            }

            with psycopg2.connect(**conf) as db:
                print(f'connect to database {os.environ["DB_NAME"]}')

                users_table = """
                CREATE TABLE users
                (
                    ID SERIAL PRIMARY KEY,
                    CreatedDate TIMESTAMP,
                    Password TEXT,
                    EMail TEXT,
                    Name TEXT,
                    Surname TEXT,
                    LastLoginDate TIMESTAMP
                );
                """

                sessions_table = """
                CREATE TABLE sessions
                (
                    ID SERIAL PRIMARY KEY,
                    CreatedDate TIMESTAMP,
                    UUID TEXT,
                    ExpirationDate TIMESTAMP,
                    UserID INT REFERENCES users(ID)
                )    
                """

                c = db.cursor()
                c.execute('DROP TABLE IF EXISTS users CASCADE')
                c.execute('DROP TABLE IF EXISTS sessions CASCADE')

                c.execute(users_table)
                c.execute(sessions_table)
                db.commit()

                columns = ('createddate', 'password', 'email', 'name', 'surname')
                values = (datetime.strftime(datetime.now(), dt_format), 'qwerty', 'example@test.com', 'postgres', 'post')
                c.execute(sql.SQL('INSERT INTO public."users" ({}) VALUES ({})').format(
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(map(sql.Literal, values))
                ))

        except psycopg2.OperationalError as e:
            print('oops')
            print(str(e.pgcode))
            print(e)
