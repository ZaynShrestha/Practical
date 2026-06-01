# Task 2: Design a Data Quality Audit System on Top of an ETL Pipeline
# Instead of just cleaning data silently, your task is to build a data quality reporting layer around a full ETL pipeline:
# Fetch 100 posts from https://jsonplaceholder.typicode.com/posts and load into Pandas
# Before cleaning, programmatically detect and record every issue found — null counts per column, duplicate row count, type mismatches, out-of-range values, and inconsistent string formats
# Apply all necessary transformations and enrichments (word count, title casing, filtering, ranking)
# After cleaning, generate a structured audit report (saved as a .csv or printed as a formatted table) showing: how many issues existed, how many were fixed, and what the before/after row count is
# Load the clean data into SQLite

import requests
import pandas as pd
import mysql.connector

def extract():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def audit(df, stage="raw"):
    report = {
        "stage": stage,
        "nulls": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "types": df.dtypes.astype(str).to_dict(),
        "row_count": len(df)
    }
    return pd.DataFrame([report])

def transform(df):
    df["word_count"] = df["body"].apply(lambda x: len(str(x).split()))
    df["title"] = df["title"].str.title()
    df = df[df["title"].notnull()]
    df["rank"] = df["word_count"].rank(method="dense", ascending=False).astype(int)
    return df

def audit_cleaned(df):
    return audit(df, stage="cleaned")

def generate_report(raw_audit, clean_audit):
    report = pd.concat([raw_audit, clean_audit], ignore_index=True)
    report.to_csv("audit_report.csv", index=False)
    print(report)


def load(df):
    conn = mysql.connector("etl_audit.db")
    df.to_sql("posts", conn, if_exists="replace", index=False)
    conn.close()
    
def run_pipeline():
    df_raw = extract()
    raw_audit = audit(df_raw, "raw")

    df_clean = transform(df_raw)
    clean_audit = audit_cleaned(df_clean)

    generate_report(raw_audit, clean_audit)
    load(df_clean)

    print("Pipeline complete. Data and audit report saved.")
