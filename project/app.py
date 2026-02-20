from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import date
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"

DATABASE = "habits.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Home route
@app.route("/")
def index():
    return render_template("index.html")



# Register
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


# Login
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


# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# Dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()

    habits = db.execute(
        "SELECT * FROM habits WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()

    habits_data = []

    for habit in habits:
        streak = calculate_streak(habit["id"])
        completion_rate = calculate_completion_rate(habit["id"])
        risk = detect_risk(habit["id"])
        weekly_data = get_weekly_data(habit["id"])

        habits_data.append({
            "id": habit["id"],
            "name": habit["name"],
            "category": habit["category"],
            "difficulty": habit["difficulty"],
            "streak": streak,
            "completion_rate": completion_rate,
            "risk": risk,
            "weekly_data": weekly_data
        })

    return render_template("dashboard.html", habits=habits_data)




# Add habit
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



def get_weekly_data(habit_id):
    db = get_db()
    today = date.today()
    week_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        log = db.execute(
            "SELECT completed FROM logs WHERE habit_id = ? AND date = ?",
            (habit_id, day)
        ).fetchone()

        if log and log["completed"] == 1:
            week_data.append(1)
        else:
            week_data.append(0)

    return week_data


# Complete habit
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


# Streak calculation
def calculate_streak(habit_id):
    db = get_db()
    logs = db.execute(
        "SELECT date FROM logs WHERE habit_id = ? ORDER BY date DESC",
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

def calculate_completion_rate(habit_id):
    db = get_db()

    total = db.execute(
        "SELECT COUNT(*) as count FROM logs WHERE habit_id = ?",
        (habit_id,)
    ).fetchone()["count"]

    if total == 0:
        return 0

    completed = db.execute(
        "SELECT COUNT(*) as count FROM logs WHERE habit_id = ? AND completed = 1",
        (habit_id,)
    ).fetchone()["count"]

    return round((completed / total) * 100, 2)


def detect_risk(habit_id):
    db = get_db()

    recent_logs = db.execute(
        "SELECT completed FROM logs WHERE habit_id = ? ORDER BY date DESC LIMIT 5",
        (habit_id,)
    ).fetchall()

    if len(recent_logs) < 3:
        return False

    missed = sum(1 for log in recent_logs if log["completed"] == 0)

    completion_rate = calculate_completion_rate(habit_id)

    if missed >= 2 or completion_rate < 40:
        return True

    return False

@app.route("/delete/<int:habit_id>")
@login_required
def delete_habit(habit_id):
    db = get_db()
    db.execute("DELETE FROM logs WHERE habit_id = ?", (habit_id,))
    db.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    db.commit()
    return redirect("/dashboard")




if __name__ == "__main__":
    app.run(debug=True)
