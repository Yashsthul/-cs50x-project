# -cs50x-project

🤖 My Final project for the CS50x course.

🏗 Habit Builder with Behavioral Analytics.

🧠 Video Demo:  <URL HERE>.

🔥 Description:

    Habit Builder with Behavioral Analytics is a full-stack web application designed to help users develop and maintain positive habits through structured tracking and intelligent data analysis. While many habit tracking applications simply allow users to mark tasks as complete, this project goes further by incorporating behavioral analytics, streak tracking algorithms, and risk detection logic to provide meaningful insights into consistency patterns.

    The motivation behind this project stems from a common real-world problem: people often begin new habits with enthusiasm but struggle to maintain long-term consistency. Traditional trackers act as digital checklists but rarely provide analytical feedback that helps users understand why they are succeeding or failing. This application addresses that gap by combining tracking, data visualization, and predictive indicators into a unified productivity platform.

🔹 Core Features

    User registration and secure login system

    Password hashing using Werkzeug security

    Session-based authentication and route protection

    Create, edit, and delete habits

    Assign category and difficulty level to each habit

    Daily habit completion logging

    Prevention of duplicate daily entries

    Current streak calculation

    Longest streak calculation

    Completion rate percentage tracking

    Weekly progress visualization using Chart.js

    Behavioral risk detection for declining habits

🔹 Habit Attributes

    Each habit includes:

    Name

    Category (Health, Productivity, Learning, Fitness, Custom)

    Difficulty level (1–5)

    Creation timestamp

🔹 Behavioral Analytics Metrics

    The dashboard displays:

    Overall completion rate percentage

    Weekly completion trends

    Most consistent habit

    Most missed habit

    Total active habits

    Current streak

    Longest streak

    Habit risk warning alerts

🔹 Technical Stack

    Backend

    Python

    Flask

    SQLite database

    Jinja templating

    Custom streak-calculation algorithms

    Frontend

    HTML

    CSS

    JavaScript

    Chart.js for visualization

    Security

    Password hashing

    Session management

    Protected routes

    Input validation
    