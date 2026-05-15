# Task 05: Full ETL System  [Hard — Month 1 Capstone]
# Bring together everything from Week 1 → 2 → 3 → 4 in one complete automated pipeline
# Goal: Build a fully automated, reusable ETL pipeline that you could run every day to get fresh data.

# Week1 : File Handling, Week2: API + requests, Week3: SQLite, Week4: Pandas + ETL

# Must: EXTRACT from at least 1 real public API with full error handling
# Must: Load into Pandas — clean nulls, duplicates, types, and string issues
# Must: TRANSFORM — add at least 2 calculated/enriched columns
# Must: LOAD to SQLite using df.to_sql() AND export to clean CSV
# Must: Write reusable functions: extract(), transform(), load() — not one big block
# Should: Add logging — print what each step is doing and how many rows
# Bonus: Run full pipeline twice — 2nd run should not create duplicate rows


import requests
import pandas as pd
import sqlite3
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract():
    logging.info("Starting data extraction...")
    try:
        res = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
        res.raise_for_status()
        data = res.json()
        logging.info(f"Extracted {len(data)} rows from API.")
        return pd.DataFrame(data)
    except Exception as e:
        logging.error(f"API extraction failed: {e}")
        return pd.DataFrame()


def transform(df):
    logging.info("Starting data transformation...")

    if df.empty:
        logging.warning("No data to transform.")
        return df

    # Clean nulls, duplicates, types
    df = df.dropna().drop_duplicates()
    df["id"] = df["id"].astype(int)
    df["userId"] = df["userId"].astype(int)

    # Enrich: add title_length and word_count
    df["title_length"] = df["title"].str.len()
    df["word_count"] = df["body"].str.split().str.len()

    logging.info(f"Transformed dataset with {len(df)} rows.")
    return df

def load(df):
    logging.info("Starting data load...")

    if df.empty:
        logging.warning("No data to load.")
        return

    # Save to CSV
    df.to_csv("etl_clean_posts.csv", index=False)
    logging.info("Saved to etl_clean_posts.csv")

    # Save to SQLite
    conn = sqlite3.connect("etl_pipeline.db")
    # Prevent duplicates: replace existing rows by primary key
    df.to_sql("posts", conn, if_exists="replace", index=False)
    conn.close()
    logging.info("Saved to etl_pipeline.db (SQLite)")

def run_pipeline():
    logging.info("=== Running ETL Pipeline ===")
    df = extract()
    df = transform(df)
    load(df)
    logging.info("=== Pipeline Completed ===")


if __name__ == "__main__":
    run_pipeline()
    run_pipeline()
