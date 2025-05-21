
from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'sql12.freesqldatabase.com',
    'user': 'sql12780377',
    'password': 'cT58Fq759x',
    'database': 'sql12780377',
    'port': 3306
}

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        uname = request.form["username"]
        pwd = request.form["password"]
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (uname, pwd))
            result = cursor.fetchone()
            message = "Login Successful!" if result else "Invalid Credentials"
        except Exception as e:
            message = "Error: " + str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template_string("""
    <html><head><title>Login</title><style>
    body { font-family: Arial; margin: 40px; }
    input { margin: 5px; padding: 5px; }
    </style></head><body>
    <h2>User Login</h2>
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <button type="submit">Login</button>
    </form>
    <p>{{ message }}</p>
    </body></html>
    """, message=message)
        