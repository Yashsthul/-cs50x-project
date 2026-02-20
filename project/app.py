from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date, timedelta
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "habits.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if not exist
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            category TEXT,
            difficulty INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT,
            completed INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ======================
# ROUTES
# ======================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Registered successfully!")
            return redirect("/login")
        except:
            flash("Username already exists")
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/dashboard")
        else:
            flash("Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    habits = conn.execute("SELECT * FROM habits WHERE user_id = ?", (session["user_id"],)).fetchall()

    enriched_habits = []

    for habit in habits:
        habit_id = habit["id"]

        today = date.today()
        week_dates = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

        weekly_data = []
        for d in week_dates:
            log = conn.execute(
                "SELECT completed FROM logs WHERE habit_id = ? AND date = ?",
                (habit_id, d)
            ).fetchone()
            weekly_data.append(log["completed"] if log else 0)

        streak = 0
        for d in reversed(week_dates):
            log = conn.execute(
                "SELECT completed FROM logs WHERE habit_id = ? AND date = ?",
                (habit_id, d)
            ).fetchone()
            if log and log["completed"] == 1:
                streak += 1
            else:
                break

        completion_rate = int((sum(weekly_data) / 7) * 100)

        enriched_habits.append({
            "id": habit["id"],
            "name": habit["name"],
            "category": habit["category"],
            "difficulty": habit["difficulty"],
            "weekly_data": weekly_data,
            "streak": streak,
            "completion_rate": completion_rate,
            "risk": completion_rate < 40
        })

    conn.close()
    return render_template("dashboard.html", habits=enriched_habits)

@app.route("/add_habit", methods=["POST"])
def add_habit():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    category = request.form["category"]
    difficulty = request.form["difficulty"]

    conn = get_db()
    conn.execute(
        "INSERT INTO habits (user_id, name, category, difficulty) VALUES (?, ?, ?, ?)",
        (session["user_id"], name, category, difficulty)
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")

@app.route("/complete/<int:habit_id>")
def complete(habit_id):
    today = date.today().isoformat()
    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM logs WHERE habit_id = ? AND date = ?",
        (habit_id, today)
    ).fetchone()

    if not existing:
        conn.execute(
            "INSERT INTO logs (habit_id, date, completed) VALUES (?, ?, 1)",
            (habit_id, today)
        )
        conn.commit()

    conn.close()
    return redirect("/dashboard")

@app.route("/delete/<int:habit_id>")
def delete(habit_id):
    conn = get_db()
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.execute("DELETE FROM logs WHERE habit_id = ?", (habit_id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)