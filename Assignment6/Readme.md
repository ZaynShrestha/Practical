📊 Month 1 · Data Engineering Pipeline

This repository showcases my progress through Month 1 of the Data Engineering journey.
Across five tasks, I built every layer of a real ETL pipeline — from cleaning raw CSVs to designing a reusable automated system.

🚀 Task 01 · Cleaning a Messy CSV

I created a deliberately messy dataset of student scores with missing values, duplicates, inconsistent casing, string‑typed numbers, extra spaces, and invalid negative scores.
Using Pandas, I applied all six cleaning techniques to fix these issues, then added a grade column based on score thresholds.
The result was a clean, reliable dataset (clean_students.csv) ready for analysis.

🌐 Task 02 · API ETL

I extracted 100 posts from the JSONPlaceholder API, transformed them by keeping only relevant fields, added a word_count column, filtered short titles, and standardized text formatting.
The cleaned dataset was saved both to CSV and SQLite, demonstrating how to move seamlessly from raw API data into structured storage.

🔗 Task 03 · Multi‑Source ETL

I combined two different API endpoints — users and posts — into one unified dataset.
This involved normalizing nested JSON fields, merging on user IDs, counting posts per user, and cleaning text fields.
The final dataset (merged_data.csv and merged.db) provided a complete view of users and their activity, with enrichment from todos to calculate completion rates.

📈 Task 04 · Transform & Enrich

Here I focused purely on transformation.
Starting with the cleaned student dataset, I engineered new columns (grade, passed, score_category, rank), produced groupby summaries, and created pivot tables for deeper insights.
This task highlighted how Pandas can be used not just for cleaning but for feature engineering and enrichment.

🛠 Task 05 · Full ETL System (Capstone)

Finally, I brought everything together into a reusable ETL pipeline.
I wrote modular functions (extract(), transform(), load()), added logging for transparency, and ensured duplicate prevention when running multiple times.
The pipeline fetches fresh data daily, cleans and enriches it, and saves outputs to both CSV and SQLite — a professional‑grade workflow.

✅ Month 1 Summary

By the end of Month 1, I had built:

A CSV cleaning workflow for messy data.

An API ETL pipeline with Pandas + SQLite.

A multi‑source merge combining users and posts.

A transform/enrich step with advanced column engineering.

A full automated ETL system with logging and duplicate prevention.

Together, these tasks form a complete data engineering foundation.
