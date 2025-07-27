import psycopg2
from psycopg2 import Error
import random
import string


def db_connect():
    return psycopg2.connect(
        user = "postgres",
        password = "12345",
        host = "localhost",
        port = "5432",
        database = "shorturl"
        )

def user_register(user_name,user_password,register_date):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        query = """
            INSERT INTO users (user_name, user_password, register_date) VALUES (%s,%s,%s)
        """
        cursor.execute(query, (user_name, user_password, register_date))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:",error)
        return False
    finally:
        if cursor : cursor.close()
        if connection : connection.close()

def user_login(user_name, user_password):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        query = """
            SELECT (user_name, user_password) FROM users VALUES(%s,%s)
        """
        cursor.execute(query, (user_name, user_password))
        connection.commit()
        return True
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()


def shorten_links(original_url, shortened_url):
    characters = string.ascii_letters + string.digits
    domain = 'https://short.url/'
    length = 6
    shortened_url = domain + ''.join(random.choices(characters, k=length))
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        query = """
            INSERT INTO url (original_url, shortened_url) VALUES(%s,%s)
        """ 
        cursor.execute(query, (original_url, shortened_url))
        connection.commit()
        return shortened_url
    except (Exception, Error) as error:
        print("Database Error:",error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

