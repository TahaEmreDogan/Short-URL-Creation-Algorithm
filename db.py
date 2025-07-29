import psycopg2
from psycopg2 import Error
import random
import string
from datetime import datetime

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

        login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
            SELECT user_id FROM users WHERE user_name = %s AND user_password = %s;
        """
        cursor.execute(query, (user_name, user_password))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]

            insert_query = """
                INSERT INTO users_login (user_id, login_date) VALUES (%s, %s);
            """
            cursor.execute(insert_query, (user_id, login_date))
            connection.commit()
            return True
        else:
            return False
    except (Exception, Error) as error:
        print("Database Error:", error)
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def add_users_links(user_id ,user_link, user_shortened_link,user_name, user_password):
    login_result = user_login(user_name, user_password)
    if login_result:
        connection = None
        cursor = None
        try:
            connection = db_connect()
            cursor = connection.cursor()
            query = """
                INSERT INTO user_login (user_id, user_link, user_shortened_link) VALUES(%s,%s,%s)
            """
            cursor.execute(query, (user_id, user_link, user_shortened_link))
            connection.commit()
            return True
        except(Exception, Error) as error:
            print("Database Error:", error)
            return False
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    else:   
        return None
    

def shorten_links(user_id , original_url, shortened_url):
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
            INSERT INTO url (user_id, original_url, shortened_url) VALUES(%s,%s,%s)
        """ 
        cursor.execute(query, (user_id, original_url, shortened_url))
        connection.commit()
        return shortened_url
    except (Exception, Error) as error:
        print("Database Error:",error)
        return False
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

def get_user_links(user_name):
    connection = None
    cursor = None
    try:
        connection = db_connect()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_name = %s", (user_name,))
        user = cursor.fetchone()
        if not user:
            return []
        user_id = user[0]
        cursor.execute("SELECT original_url, shortened_url FROM url WHERE user_id = %s", (user_id,))
        links = cursor.fetchall()
        return links
    except (Exception, Error) as error:
        print("Database Error:", error)
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

