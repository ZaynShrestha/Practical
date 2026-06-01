📦 Fault-Tolerant ETL & Data Quality Capstone
🚀 Overview
This repository contains a Month 1 ETL Capstone Project with three progressively complex tasks:

Multi-Source ETL Pipeline with Conflict Resolution

Data Quality Audit System

Modular, Logged ETL System with Full Enrichment and Idempotency

The project demonstrates how to build robust ETL pipelines using Python, Pandas, MySQL, and Requests, with proper error handling, conflict resolution, data cleaning, audit reporting, and production-style modularity.

🛠 Task 1: Multi-Source ETL Pipeline
Steps Implemented
Extract:

Public API: https://jsonplaceholder.typicode.com/users and /posts

Local messy CSV file

Error handling: retries, timeouts, HTTP status checks

Normalize:

Flatten nested JSON fields (e.g., address.city) using pd.json_normalize()

Merge with Conflict Resolution:

Shared key: email

Rule: If the same email exists in both sources but names differ → API wins (assumed fresher data). Conflicts are logged.

Clean (6 techniques):

Handle nulls

Remove duplicates

Standardize casing

Fix types

Strip whitespace

Detect/remove outliers

Load:

Save unified dataset to MySQL and CSV

Ensure idempotency: second run does not insert duplicate rows

📊 Task 2: Data Quality Audit System
Steps Implemented
Extract:

100 posts from https://jsonplaceholder.typicode.com/posts

Audit:

Null counts per column

Duplicate row count

Type mismatches

Out-of-range values

Inconsistent string formats

Transform & Enrich:

Word count per post

Title casing

Filtering & ranking

Audit Report:

Structured CSV report showing:

Issues detected

Issues fixed

Before/after row counts

Load:

Clean data stored in MySQL

🚀 Task 3: Modular, Logged ETL System (Capstone)
Architecture
Functions:

extract(): API call with retries, timeouts, status checks

clean(): Deduplication, null handling, type fixes

transform(): Adds 3+ calculated columns (word count, score category, rank)

load(): Saves to CSV and MySQL with idempotency

Logging:

Each function logs what it is doing, rows in/out

Transformations:

Word count

Title casing

Score category (short/medium/long)

Summary Table:

groupby() with mean, min, max per category

Load:

CSV (index=False)

SQLite (df.to_sql() with duplicate prevention)
