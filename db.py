import psycopg2
from psycopg2 import Error

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