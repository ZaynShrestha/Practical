
📊 Data Engineering & Python SQL Projects

This repository contains a series of mini data engineering projects built using Python, SQL (SQLite/MySQL), and public APIs. The projects focus on real-world skills such as database design, API integration, data cleaning, querying, and automation pipelines.

🚀 Project Overview

This project includes 5 structured tasks that gradually build skills from basic SQL operations to a complete automated data pipeline system.

🧩 Tasks Included
📘 Task 1: Create, Insert & Query (Library Database)

Goal: Learn SQL basics using a books database.

Features:
Create SQLite database (library.db)
Create books table
Insert sample book records (8+ entries)
Run SQL queries:
Books published after 2000 (sorted by rating)
Fiction books with rating > 4.0
Average book rating
Count of books per genre (GROUP BY)
Skills learned:
SQL SELECT, WHERE, ORDER BY
Aggregation (AVG, COUNT)
GROUP BY queries

🌐 Task 2: API → MySQL/SQLite Pipeline

Goal: Fetch API data and store it in a structured database.

Features:
Fetch users from:
https://jsonplaceholder.typicode.com/users
Create app.db
Store:
name, email, phone
nested JSON extraction (city, company name)
Handle errors during insertion
Create second table posts
Store posts for user_id 1, 2, 3
Queries:
Alphabetical user listing
Users grouped by city (HAVING COUNT > 1)
Skills learned:
API integration (requests)
JSON parsing (nested data)
Database normalization
Error handling

🌦 Task 3: Weather Data Analysis System

Goal: Build a real-world weather analytics pipeline.

Features:
Fetch 7-day forecast using Open-Meteo API
Cities used:
Kathmandu
Pokhara
Biratnagar
Store in weather.db
Columns:
city, date, max_temp, min_temp
Queries:
City with highest average temperature
Hottest single day overall
Days with temperature difference > 10°C
Output:
Generates summary.txt report
Skills learned:
Real-time API usage
Data aggregation
File handling (TXT reports)
Comparative analysis

🎓 Task 4: Student Grade Management System

Goal: Perform full CRUD operations with data validation.

Features:
Create grades.db
Store student records (15 entries)
Grade system function:
A / B / C / D / F based on score
Update grades dynamically
Delete failed students (score < 50)
Add passed column using ALTER TABLE
Prevent duplicate student entries
Queries:
Count students per grade (A → F)
Skills learned:
CRUD operations (Create, Read, Update, Delete)
Data validation
Schema modification (ALTER TABLE)
Business logic in Python + SQL

🔁 Task 5: Full Automation System (Capstone Project)

Goal: Build a complete automated data pipeline.

Features:
Fetch data from public APIs
Error handling using try/except
Store structured data in database
Run multiple SQL analytics queries
Export results to:
CSV file
TXT report
Functions used:
fetch_data()
store_data()
run_report()
Bonus:
Fully modular pipeline
Can be executed in a single run
🛠 Tech Stack
Python 🐍
SQLite / MySQL 🗄️
REST APIs 🌐
Requests Library
CSV & File Handling
📂 Project Structure
project/
│
├── task1_library.py
├── task2_api_pipeline.py
├── task3_weather.py
├── task4_grades.py
├── task5_capstone.py
│
├── library.db
├── app.db
├── weather.db
├── grades.db
│
├── summary.txt
├── report.csv
└── README.md

📈 Key Learning Outcomes
SQL database design and querying
API integration and automation
Real-world data extraction and transformation
Error handling and data validation
Building ETL-style pipelines in Python
Exporting structured reports

🚀 How to Run
# Install dependencies
pip install requests

# Run any task
python task1_library.py
python task2_api_pipeline.py
python task3_weather.py
python task4_grades.py
python task5_capstone.py
