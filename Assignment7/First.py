# Task 1: Build a Fault-Tolerant Multi-Source ETL Pipeline with Conflict Resolution
# You are given two data sources — a live public API (/users and /posts from JSONPlaceholder) and a locally generated messy CSV file. Your task is to:
# Extract data from both sources simultaneously using proper error handling (timeouts, retries, HTTP error codes)
# Normalize nested JSON fields (e.g., address.city) using pd.json_normalize()
# Merge the two DataFrames on a shared key, but handle conflicts — what happens when the same email appears in both sources with different name values? Write logic to decide which one wins and document your decision
# After merging, apply all 6 cleaning techniques (nulls, duplicates, casing, types, whitespace, outliers)
# Load the final unified dataset to both SQLite and CSV
# On a second run of your script, no duplicate rows should be inserted into SQLite

import mysql.connector
import pandas as pd
import logging
from requests.adapters import HTTPAdapter, Retry


def get_mysql_connection():
    return mysql.connector.connect(


        host="localhost",       # or your DB server
        user="root",            # your MySQL username         
        password="Root@#$#1",
        database="audit_etl"       # make sure this DB exists
    )

def load_to_mysql(df, table_name="unified_data"):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT,
            name VARCHAR(100),
            email VARCHAR(100),
            city VARCHAR(100),
            title TEXT
        )
    """)

    # Insert rows (replace duplicates by primary key if needed)
    for _, row in df.iterrows():
        cursor.execute(f"""
            REPLACE INTO {table_name} (id, name, email, city, title)
            VALUES (%s, %s, %s, %s, %s)
        """, (row["id"], row["name"], row["email"], row["city"], row["title"]))

    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"Saved {len(df)} rows into MySQL table {table_name}.")
