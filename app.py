from flask import Flask, request, render_template_string, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secure_random_secret"  # Required for session management

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
            if result:
                session['username'] = uname
                return redirect(url_for('dashboard'))
            else:
                message = "❌ Invalid Credentials"
        except Exception as e:
            message = "Error: " + str(e)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template_string("""
    <html><head><title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); width: 300px; }
        h2 { text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; }
        p { text-align: center; color: red; }
    </style>
    </head><body>
    <div class="login-container">
        <h2>User Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required><br>
            <input name="password" type="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <p>{{ message }}</p>
    </div>
    </body></html>
    """, message=message)

@app.route("/dashboard")
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template_string("""
    <html><head><title>Dashboard</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background-color: #e0f7fa; }
        h1 { color: #00796b; }
    </style>
    </head><body>
        <h1>Welcome, {{ user }}!</h1>
        <p>You have successfully logged in.</p>
    </body></html>
    """, user=session['username'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
