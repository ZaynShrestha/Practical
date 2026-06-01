#  Task 3: Build a Modular, Logged ETL System with Full Enrichment and Idempotency
# This is your Month 1 capstone challenge. Design a production-style ETL system with the following strict requirements:
# Structure your code into four separate reusable functions: extract(), clean(), transform(), load() — each must be independently callable and testable
# Extract data from at least one real public API with full error handling (try/except, timeout, status code checks)
# In the transform step, engineer at least 3 new calculated columns (e.g., grade, rank, score category, word count, pass/fail, completion rate)
# Use groupby() to produce a printed summary table — mean, min, max grouped by at least one categorical column
# Add logging throughout — every function must print what it is doing, how many rows it received, and how many rows it output
# Load to both CSV (index=False) and SQLite using df.to_sql() — and ensure running the full pipeline twice does not create duplicate rows in the database
 
import requests
import pandas as pd
import mysql.connector
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_NAME = "audit_etl"
CSV_FILE = "output.csv"


def extract(url):
    logging.info("Starting data extraction")

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logging.error(f"Failed API call. Status code: {response.status_code}")
            return pd.DataFrame()

        data = response.json()
        df = pd.DataFrame(data)

        logging.info(f"Extracted {len(df)} rows successfully.")
        return df

    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
        return pd.DataFrame()

    except Exception as e:
        logging.error(f"Unexpected error during extraction: {e}")
        return pd.DataFrame()


def clean(df):
    logging.info("Starting data cleaning")

    if df.empty:
        logging.warning("Empty DataFrame received in clean().")
        return df

    initial_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values (basic fill)
    df = df.fillna({
        "title": "no_title",
        "body": "no_body"
    })

    # Ensure correct types
    df["id"] = df["id"].astype(int)
    df["userId"] = df["userId"].astype(int)

    logging.info(f"Cleaned data: {initial_rows} → {len(df)} rows")
    return df


def transform(df):
    logging.info("Starting data transformation...")

    if df.empty:
        return df

    # Feature 1: word count of post body
    df["word_count"] = df["body"].apply(lambda x: len(str(x).split()))

    # Feature 2: score based on word count
    df["score"] = df["word_count"] * 2

    # Feature 3: category
    df["category"] = df["word_count"].apply(
        lambda x: "short" if x < 20 else "medium" if x < 40 else "long"
    )

    # Feature 4: rank inside each user
    df["rank"] = df.groupby("userId")["score"].rank(ascending=False)

    logging.info(f"Transformation complete. Rows: {len(df)}")

    # GROUPBY SUMMARY (required)
    summary = df.groupby("category")["score"].agg(["mean", "min", "max"])
    print("\nGROUPBY SUMMARY (score by category) ")
    print(summary)

    return df


def load(df):
    logging.info("Starting load process...")

    if df.empty:
        logging.warning("No data to load.")
        return

    # ---------- CSV ----------
    df.to_csv(CSV_FILE, index=False)
    logging.info(f"Data written to CSV: {CSV_FILE}")

    # ---------- mySQL ----------
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@#$#1",
    database="audit_etl"
)
    
    cursor = conn.cursor()

    # Create table with UNIQUE constraint for id (idempotency)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            userId INTEGER,
            id INTEGER PRIMARY KEY,
            title TEXT,
            body TEXT,
            word_count INTEGER,
            score INTEGER,
            category TEXT,
            student_rank REAL
        )
    """)

    # Insert without duplicates
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO posts (
                    userId, id, title, body,
                    word_count, score, category, rank
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["userId"],
                row["id"],
                row["title"],
                row["body"],
                row["word_count"],
                row["score"],
                row["category"],
                row["rank"]
            ))
        except Exception as e:
            logging.error(f"Insert error: {e}")

    conn.commit()
    conn.close()

    logging.info("Load complete (CSV + SQLite).")

def run_pipeline():
    logging.info("ETL PIPELINE STARTED")

    url = "https://jsonplaceholder.typicode.com/posts"

    df = extract(url)
    df = clean(df)
    df = transform(df)
    load(df)

    logging.info("ETL PIPELINE FINISHED")


if __name__ == "__main__":
    run_pipeline()