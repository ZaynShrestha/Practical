##Task2:  API → MySQL Pipeline
#Ques: Fetch user data from an API, store it in MySQL, and query it — complete automated pipeline.
#1. Fetch all users from https://jsonplaceholder.typicode.com/users
#2. Create app.db with a users table: id, name, email, phone, city, company_name
#3. Extract city from address.city and company name from company.name (nested JSON!)
#4. Insert all 10 users into the database with proper error handling
#5. Query 1: Print all users sorted alphabetically by name
#6. Query 2: Find users from the same city (GROUP BY city, HAVING COUNT > 1)
#7. Add a second table posts — fetch from /posts and insert only posts by user_id 1, 2, and 3

import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@#$#1"
)

cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

#Create Table:


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    city VARCHAR(100),
    company_name VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INT PRIMARY KEY,
    user_id INT,
    title TEXT,
    body TEXT
)
""")

#Fetch Users API:


print("Fetching users...")

users_url = "https://jsonplaceholder.typicode.com/users"
users_data = requests.get(users_url).json()

#Insert Users:

for u in users_data:
    try:
        cursor.execute("""
            INSERT INTO users (id, name, email, phone, city, company_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            u["id"],
            u["name"],
            u["email"],
            u["phone"],
            u["address"]["city"],       # nested JSON
            u["company"]["name"]        # nested JSON
        ))
    except Exception as e:
        print("User insert error:", e)

conn.commit()

#Fetch post API:

print("Fetching posts...")

posts_url = "https://jsonplaceholder.typicode.com/posts"
posts_data = requests.get(posts_url).json()

# only user_id 1,2,3

for p in posts_data:
    if p["userId"] in [1, 2, 3]:
        try:
            cursor.execute("""
                INSERT INTO posts (id, user_id, title, body)
                VALUES (%s, %s, %s, %s)
            """, (
                p["id"],
                p["userId"],
                p["title"],
                p["body"]
            ))
        except Exception as e:
            print("Post insert error:", e)

conn.commit()


#Query Function:

def show(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

#Query sort Users:

show(
    "Users sorted alphabetically",
    "SELECT * FROM users ORDER BY name ASC"
)

#Query : same city Users:

show(
    "Cities with more than 1 user",
    """
    SELECT city, COUNT(*) AS total_users
    FROM users
    GROUP BY city
    HAVING COUNT(*) > 1
    """
)

#Show posts:

show(
    "Posts (user_id 1,2,3)",
    "SELECT * FROM posts ORDER BY user_id"
)

conn.close()

print("\n Pipeline Completed Successfully!")