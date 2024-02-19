import psycopg2

from config import config


def create_database(db_name):
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()


def create_tables(db_name):
    conn = psycopg2.connect(dbname=db_name, **config())
    with conn:
        with conn.cursor() as cur:
            cur.execute('CREATE TABLE employers'
                        '('
                        'id int PRIMARY KEY,'
                        'name varchar(255) UNIQUE NOT NULL'
                        ')')
            cur.execute('CREATE TABLE vacancies'
                        '('
                        'id int PRIMARY KEY,'
                        'name varchar(255) NOT NULL,'
                        'area varchar(255),'
                        'salary_from int,'
                        'salary_to int,'
                        'published_at timestamp,'
                        'url varchar(255),'
                        'employer int REFERENCES employers(id) NOT NULL'
                        ')')
    conn.close()

