from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "habits.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        hash_pw = generate_password_hash(password)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
                (username, email, hash_pw)
            )
            db.commit()
        except:
            flash("Username or email already exists.")
            return redirect("/register")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            return redirect("/dashboard")

        flash("Invalid credentials.")
        return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    habits = db.execute(
        "SELECT * FROM habits WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()

    return render_template("dashboard.html", habits=habits)

@app.route("/add_habit", methods=["POST"])
@login_required
def add_habit():
    name = request.form.get("name")
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")

    db = get_db()
    db.execute(
        "INSERT INTO habits (user_id, name, category, difficulty) VALUES (?, ?, ?, ?)",
        (session["user_id"], name, category, difficulty)
    )
    db.commit()

    return redirect("/dashboard")

@app.route("/complete/<int:habit_id>")
@login_required
def complete(habit_id):
    today = date.today()

    db = get_db()

    existing = db.execute(
        "SELECT * FROM logs WHERE habit_id = ? AND date = ?",
        (habit_id, today)
    ).fetchone()

    if not existing:
        db.execute(
            "INSERT INTO logs (habit_id, date, completed) VALUES (?, ?, 1)",
            (habit_id, today)
        )
        db.commit()

    return redirect("/dashboard")

def calculate_streak(habit_id):
    db = get_db()
    logs = db.execute(
        "SELECT date FROM logs WHERE habit_id = ? AND completed = 1 ORDER BY date DESC",
        (habit_id,)
    ).fetchall()

    streak = 0
    previous_date = date.today()

    for log in logs:
        log_date = date.fromisoformat(log["date"])

        if (previous_date - log_date).days <= 1:
            streak += 1
            previous_date = log_date
        else:
            break

    return streak
