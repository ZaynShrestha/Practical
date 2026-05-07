# #Task 2 · API Monitor with Change Detection [Hard]

# Using mysql-connector-python and https://jsonplaceholder.typicode.com/posts, build a monitoring script that detects 
# changes between runs. Create a database called monitor_db with two tables — posts (stores fetched data) and change_log 
# (records what changed and when). On first run, insert all posts and log each as 'NEW'. Then manually update one row in 
# MySQL (UPDATE posts SET title='Changed' WHERE id=1) and re-run — your script must detect the mismatch and log it as 
# 'MODIFIED' in change_log. Print results for: post count per user, all change log entries from the latest run, and 
# which user triggered the most change events. Wrap every API call and DB operation in try/except with printed error messages.

# Deliverable: MySQL monitor_db with both tables populated + Python script


import requests
import mysql.connector
from datetime import datetime

def get_conn():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@#$#1"
        )
        return conn
    except mysql.connector.Error as e:
        print("DB Connection Error:", e)
        return None

def setup_db():
    conn = get_conn()
    if not conn:
        return None, None

    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS monitor_db")
        cursor.execute("USE monitor_db")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INT PRIMARY KEY,
            userId INT,
            title TEXT,
            body TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS change_log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            post_id INT,
            change_type VARCHAR(20),
            old_title TEXT,
            new_title TEXT,
            old_body TEXT,
            new_body TEXT,
            changed_at DATETIME
        )
        """)
        conn.commit()
    except Exception as e:
        print("DB Setup Error:", e)

    return conn, cursor

def fetch_posts():
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("API Error:", e)
        return []

def sync_posts(conn, cursor, api_data):
    print("Syncing posts...")

    try:
        cursor.execute("SELECT id, title, body FROM posts")
        db_posts = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
    except Exception as e:
        print("DB Fetch Error:", e)
        return

    for post in api_data:
        post_id = post["id"]
        title = post["title"]
        body = post["body"]

        if post_id not in db_posts:
            # NEW
            try:
                cursor.execute("""
                    INSERT INTO posts (id, userId, title, body)
                    VALUES (%s, %s, %s, %s)
                """, (post_id, post["userId"], title, body))

                cursor.execute("""
                    INSERT INTO change_log (post_id, change_type, old_title, new_title, old_body, new_body, changed_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (post_id, "NEW", None, title, None, body, datetime.now()))
            except Exception as e:
                print("Insert Error:", e)

        else:
            old_title, old_body = db_posts[post_id]
            if old_title != title or old_body != body:
                # MODIFIED
                try:
                    cursor.execute("""
                        UPDATE posts SET title=%s, body=%s WHERE id=%s
                    """, (title, body, post_id))

                    cursor.execute("""
                        INSERT INTO change_log (post_id, change_type, old_title, new_title, old_body, new_body, changed_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (post_id, "MODIFIED", old_title, title, old_body, body, datetime.now()))
                except Exception as e:
                    print("Update Error:", e)

    conn.commit()

def run_reports(cursor):
    print("\nREPORTS\n")

    try:

        # 1. Post count per user
        print("1. Post count per user")
        cursor.execute("SELECT userId, COUNT(*) FROM posts GROUP BY userId")
        for row in cursor.fetchall():
            print(row)

        # 2. Latest change log entries
        print("\n2. Change Log (latest run)")
        cursor.execute("SELECT MAX(changed_at) FROM change_log")
        latest_time = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM change_log WHERE changed_at=%s", (latest_time,))
        for row in cursor.fetchall():
            print(row)

        # 3. User with most changes
        print("\n3. User with most changes")
        cursor.execute("""
            SELECT p.userId, COUNT(*) as changes
            FROM change_log c
            JOIN posts p ON c.post_id = p.id
            GROUP BY p.userId
            ORDER BY changes DESC
            LIMIT 1
        """)
        
        print(cursor.fetchone())
    except Exception as e:
        print("Report Error:", e)

def main():
    conn, cursor = setup_db()
    if not conn:
        return

    api_data = fetch_posts()
    if not api_data:
        print("No data fetched")
        return

    sync_posts(conn, cursor, api_data)
    run_reports(cursor)

    conn.close()
    print("\nMonitoring Pipeline Completed!")

if __name__ == "__main__":
    main()
