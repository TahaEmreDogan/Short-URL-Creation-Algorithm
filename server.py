from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import psycopg2
from psycopg2 import Error
import db

def get_long_url(short_code):
    connection = None
    cursor = None
    try:
        connection = db.db_connect()
        cursor = connection.cursor()
        query = "SELECT original_url FROM url WHERE shortened_url LIKE %s"
        like_pattern = f"%/{short_code}"
        cursor.execute(query, (like_pattern,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except (Exception, Error) as error:
        print("Database Error:", error)
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        short_code = self.path.lstrip('/')
        if not short_code:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'No short code provided.')
            return

        long_url = get_long_url(short_code)
        if long_url:
            self.send_response(302)
            self.send_header('Location', long_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Short link not found.')

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RedirectHandler)
    print("Short link redirection server started (on port 8000).")
    httpd.serve_forever()
