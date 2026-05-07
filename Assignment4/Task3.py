# ##Task3: Weather Data + Analysis
# #Ques: Use the Open-Meteo API to fetch 7-day weather for 3 cities and store + compare them in MySQL.
#1. Fetch 7-day forecast (max + min temp) for 3 cities of your choice using Open-Meteo API
#2. Create weather.db with a forecasts table: id, city, date, max_temp, min_temp
#3. Insert all 21 rows (3 cities × 7 days) into the database
#4. Query 1: Which city has the highest average max temperature?
#5. Query 2: Find the single hottest day across all 3 cities
#6. Query 3: Find days where the temperature difference (max - min) is greater than 10°C
#7. Save a summary report to a summary.txt file using Python file handling (Week 1 skill!)



import requests
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

#Create Database:

db_name = os.getenv("DB_NAME")
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")

#Create table:

cursor.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    date DATE,
    max_temp FLOAT,
    min_temp FLOAT
)
""")

#Cities (name, lat, lon)

cities = [
    ("Kathmandu", 27.7172, 85.3240),
    ("Delhi", 28.7041, 77.1025),
    ("Tokyo", 35.6762, 139.6503)
]

#Fetch Weather Data:

print("Fetching weather data...")

for city, lat, lon in cities:

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"

    data = requests.get(url).json()

    dates = data["daily"]["time"]
    max_temps = data["daily"]["temperature_2m_max"]
    min_temps = data["daily"]["temperature_2m_min"]

    for i in range(7):
        try:
            cursor.execute("""
                INSERT INTO forecasts (city, date, max_temp, min_temp)
                VALUES (%s, %s, %s, %s)
            """, (
                city,
                dates[i],
                max_temps[i],
                min_temps[i]
            ))
        except Exception as e:
            print("Insert error:", e)

conn.commit()

#Query Function:

def show(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

#Highest avg max temp

show(
    "City with highest average max temperature",
    """
    SELECT city, AVG(max_temp) AS avg_max
    FROM forecasts
    GROUP BY city
    ORDER BY avg_max DESC
    LIMIT 1
    """
)

#Hottest day:

show(
    "Single hottest day overall",
    """
    SELECT city, date, max_temp
    FROM forecasts
    ORDER BY max_temp DESC
    LIMIT 1
    """
)

#Large temp differences:

show(
    "Days with temp difference > 10°C",
    """
    SELECT city, date, (max_temp - min_temp) AS diff
    FROM forecasts
    WHERE (max_temp - min_temp) > 10
    """
)


cursor.execute("""
SELECT city, AVG(max_temp)
FROM forecasts
GROUP BY city
""")

avg_data = cursor.fetchall()

cursor.execute("""
SELECT city, date, max_temp
FROM forecasts
ORDER BY max_temp DESC
LIMIT 1
""")

hottest = cursor.fetchone()

cursor.execute("""
SELECT city, COUNT(*)
FROM forecasts
WHERE (max_temp - min_temp) > 10
GROUP BY city
""")

variation = cursor.fetchall()

with open("summary.txt", "w") as f:
    f.write("WEATHER ANALYSIS REPORT\n")
    f.write("="*40 + "\n\n")

    f.write("Average Max Temperature per City:\n")
    for row in avg_data:
        f.write(f"{row[0]}: {row[1]:.2f}\n")

    f.write("\nHottest Day:\n")
    f.write(f"{hottest}\n")

    f.write("\nHigh Temperature Variation Days (>10°C):\n")
    for row in variation:
        f.write(f"{row}\n")

print("\n Summary saved to summary.txt")


conn.close()