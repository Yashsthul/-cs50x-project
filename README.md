# -cs50x-project

My Final project for the CS50x course.

Habit Builder with Behavioral Analytics.

 Video Demo:  <URL HERE>.

 Description:

Habit Builder with Behavioral Analytics is a full-stack web application designed to help users develop and maintain positive habits through structured tracking and intelligent data analysis. While many habit tracking applications simply allow users to mark tasks as complete, this project goes further by incorporating behavioral analytics, streak tracking algorithms, and risk detection logic to provide meaningful insights into consistency patterns.

The motivation behind this project stems from a common real-world problem: people often begin new habits with enthusiasm but struggle to maintain long-term consistency. Traditional trackers act as digital checklists but rarely provide analytical feedback that helps users understand why they are succeeding or failing. This application addresses that gap by combining tracking, data visualization, and predictive indicators into a unified productivity platform.

Core Features
1. User Authentication

The application includes a secure user authentication system. Users can register, log in, and log out. Passwords are hashed using Flask’s Werkzeug security utilities before being stored in the database. Session management ensures that each user only accesses their own data. This demonstrates secure authentication practices and session handling learned throughout CS50.

2. Habit Management

Users can create, edit, and delete habits. Each habit includes:

Name

Category (Health, Productivity, Learning, Fitness, Custom)

Difficulty level (1–5)

Creation timestamp

Habits are stored in a relational SQL database and linked to users via foreign keys to maintain proper data relationships.

3. Daily Habit Logging

Users can mark habits as completed on a daily basis. Each completion entry is stored in a logs table, which records:

Habit ID

Date

Completion status

The system prevents duplicate entries for the same habit on the same day. This ensures database consistency and prevents inflated streak calculations.

4. Streak Tracking System

One of the most important features of the application is its streak calculation algorithm. For each habit, the system computes:

Current streak (consecutive completed days)

Longest streak achieved

The streak logic works by sorting habit logs by date and counting consecutive completed entries until a missed day is encountered. This required careful handling of date comparisons and loop control to ensure accurate calculations.

5. Behavioral Analytics Dashboard

The dashboard provides users with insights into their performance over time. Metrics include:

Overall completion rate percentage

Weekly completion visualization

Most consistent habit

Most missed habit

Total active habits

Data visualization is implemented using JavaScript and Chart.js, which dynamically renders charts based on backend data passed from Flask routes.

6. Habit Risk Detection (Advanced Feature)

A unique feature of this project is the behavioral risk detection system. The application evaluates recent activity patterns and flags habits as “at risk” if:

Two or more days were missed within the last five days

Completion rate falls below a defined threshold (e.g., 40%)

This predictive warning system transforms the application from a passive tracker into an active behavioral assistant.

Technical Architecture
Backend

The backend is built using Python and Flask. The application uses:

Flask routing

Jinja templating

Session management

SQL queries with joins

Custom Python functions for analytics

Database operations are handled using SQLite. The relational schema includes three main tables:

users

habits

logs

Each table is normalized and connected through foreign key constraints to preserve data integrity.

Frontend

The frontend consists of:

HTML templates

CSS styling

JavaScript for interactivity

Chart.js for data visualization

Templates extend a common layout.html file to maintain consistent structure and reduce repetition.

Security Considerations

Password hashing (Werkzeug)

Session-based authentication

Route protection for logged-in users only
    