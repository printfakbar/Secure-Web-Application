from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "secure123"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )
            conn.commit()
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")
    return render_template("profile.html", user=session["user"])

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        new_password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_password, session["user"])
        )

        conn.commit()

        return "Password Changed Successfully"

    return render_template("change_password.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)