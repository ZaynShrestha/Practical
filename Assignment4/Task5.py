# #Task5: The Full System [Capstone]
# #Ques:  Build a complete automated data system — fetch, store, analyse, and export. No manual steps.
# # Fetch API requests → Error handle try/except → Store MySQLmysql.connector → Analyse SQL queries → ExportCSV + TXT

# Must: Fetch data from any public API with error handling
# Must: Store ALL fetched data in a properly structured MySQL database
# Must: Run at least 3 meaningful SQL queries and print results with labels
# Must: Export query results to a CSV file (combine Week 1 + Week 3)
# Must: Handle errors at every step — API, database, file
# Should: Write reusable functions: fetch_data(), store_data(), run_report()
# Bonus: Schedule it: run the whole thing every time you run the script fresh


import requests
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

#Fetch data (API):

def fetch_data():
    print("Fetching data from API")

    try:
        url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return None

#Database connection:

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except mysql.connector.Error as e:
        print("DB Connection Error:", e)
        return None

#Store data in MySQL:

def store_data(data):
    print("Storing data in MySQL")

    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # Create DB

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

    # Create table

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        city VARCHAR(100),
        company VARCHAR(100)
    )
    """)

    # Insert data

    for user in data:
        try:
            cursor.execute("""
                INSERT INTO users (id, name, email, city, company)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user["id"],
                user["name"],
                user["email"],
                user["address"]["city"],
                user["company"]["name"]
            ))
        except mysql.connector.Error as e:
            print("Insert error:", e)

    conn.commit()
    return conn

#Run analytics queries:

def run_queries(conn):
    cursor = conn.cursor()
    cursor.execute(f"USE {DB_NAME}")

    print("\n Running SQL Reports...\n")

    # QUERY 1
    print("1Users sorted by name")
    cursor.execute("SELECT * FROM users ORDER BY name ASC")
    q1 = cursor.fetchall()
    for row in q1:
        print(row)

    # QUERY 2
    print("\n2Users per city")
    cursor.execute("""
        SELECT city, COUNT(*) 
        FROM users 
        GROUP BY city
    """)
    q2 = cursor.fetchall()
    for row in q2:
        print(row)

    # QUERY 3
    print("\n3Total users count")
    cursor.execute("SELECT COUNT(*) FROM users")
    q3 = cursor.fetchone()
    print(q3)

    return q1, q2, q3

#Export to CSV

def export_csv(data):
    print("\n Exporting CSV")

    try:
        df = pd.DataFrame(data, columns=["id", "name", "email", "city", "company"])
        filename = "users_report.csv"
        df.to_csv(filename, index=False)
        print(f"CSV saved as {filename}")

    except Exception as e:
        print("CSV Error:", e)

#Export text report:

def export_txt(q1, q2, q3):
    print("\n Creating TXT report...")

    try:
        with open("summary_report.txt", "w") as f:
            f.write("CAPSTONE REPORT\n")
            f.write("="*40 + "\n")
            f.write(f"Generated: {datetime.now()}\n\n")

            f.write("Users sorted by name:\n")
            for r in q1:
                f.write(str(r) + "\n")

            f.write("\nUsers per city:\n")
            for r in q2:
                f.write(str(r) + "\n")

            f.write("\nTotal users:\n")
            f.write(str(q3))

        print("TXT report saved")

    except Exception as e:
        print("File Error:", e)

#Main controller:

def run_pipeline():
    print("\n STARTING CAPSTONE PIPELINE...\n")

    data = fetch_data()
    if not data:
        print("Pipeline stopped due to API error")
        return

    conn = store_data(data)
    if not conn:
        print("Pipeline stopped due to DB error")
        return

    q1, q2, q3 = run_queries(conn)

    export_csv(q1)
    export_txt(q1, q2, q3)

    conn.close()

    print("\n PIPELINE COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_pipeline()