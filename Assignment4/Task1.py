## Task1: Create, Insert, & Query
#Ques: Create MySQL database, populate it with data, and run queries to answer questions about it.
#1. Create a database called library.db with a table books (id, title, author, year, genre, rating REAL)
#2. Insert at least 8 books — use a mix of genres, years, and ratings
#3. Query 1: SELECT all books published after 2000, ordered by rating (highest first)
#4. Query 2: SELECT all books in the 'Fiction' genre with rating above 4.0
#5. Query 3: Find the average rating across all books
#6. Query 4: Count how many books exist per genre — use GROUP BY genre
#7. Print all query results neatly with labels — not just raw tuples

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


cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    author VARCHAR(100),
    year INT,
    genre VARCHAR(50),
    rating FLOAT
)
""")

#Insert data only once :

cursor.execute("SELECT COUNT(*) FROM books")
count = cursor.fetchone()[0]

if count == 0:
    books_data = [
        ('The Alchemist', 'Paulo Coelho', 1988, 'Fiction', 4.2),
        ('Harry Potter', 'J.K. Rowling', 2001, 'Fantasy', 4.8),
        ('The Da Vinci Code', 'Dan Brown', 2003, 'Thriller', 4.1),
        ('Clean Code', 'Robert C. Martin', 2008, 'Programming', 4.7),
        ('The Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasy', 4.9),
        ('Atomic Habits', 'James Clear', 2018, 'Self-help', 4.6),
        ('Inferno', 'Dan Brown', 2013, 'Thriller', 3.9),
        ('Ikigai', 'Héctor García', 2016, 'Self-help', 4.3)
    ]

    cursor.executemany("""
        INSERT INTO books (title, author, year, genre, rating)
        VALUES (%s, %s, %s, %s, %s)
    """, books_data)

    conn.commit()

#Function to print result:

def run_query(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)

#Query:

run_query(
    "Books published after 2000 (highest rating first)",
    "SELECT * FROM books WHERE year > 2000 ORDER BY rating DESC"
)

run_query(
    "Fiction books with rating above 4.0",
    "SELECT * FROM books WHERE genre='Fiction' AND rating > 4.0"
)

run_query(
    "Average rating of all books",
    "SELECT AVG(rating) FROM books"
)

run_query(
    "Count of books per genre",
    "SELECT genre, COUNT(*) FROM books GROUP BY genre"
)

conn.close()