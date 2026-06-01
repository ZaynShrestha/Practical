📊 Exploratory Data Analysis (EDA) — Week 5 Capstone
🚀 Overview
This repository contains four structured EDA tasks designed to build strong data intuition and storytelling skills. Each task applies the EDA checklist and expands into deeper analysis, distribution exploration, correlation studies, and a full EDA report on real-world data.

✅ Task 01: Checklist on Your Own Data
Goal: Run the full EDA checklist on a dataset from Weeks 1–4.

Steps Implemented
Load dataset into Pandas (pd.read_csv() or pd.read_sql()).

Print df.shape, df.info(), df.dtypes — document findings in comments.

Check missing values (df.isnull().sum()).

Run df.describe() — identify 3 key observations.

Use value_counts() on at least one categorical column.

Plot histograms for numeric columns.

Plot box plots for at least 2 columns.

Write a 5-line summary comment block.

Deliverables:

.py script with all 8 steps

Charts saved as .png

Bonus: sns.pairplot() with description

🌡 Task 02: Distribution Deep Dive
Goal: Fetch weather data for 7 days across 5 cities, store in SQLite, and analyse distributions.

Steps Implemented
Fetch 7-day max/min temperatures from Open-Meteo API.

Store in weather.db (SQLite).

Load into Pandas and run EDA checklist.

Plot histogram of max temperatures across all cities.

Side-by-side box plots comparing max temps across cities.

Detect outliers using IQR method.

Plot KDE curves for each city’s temperature.

Calculate grouped summary stats (mean, median, std, min, max).

Write 5 observations.

Deliverables:

weather.db

4 charts saved as .png

Written observations

Bonus: Add rainfall data and compare

🎓 Task 03: Correlation Analysis
Goal: Create a synthetic student dataset and analyse correlations.

Steps Implemented
Create students.csv with 50 students:

Columns: name, study_hours, sleep_hours, attendance_pct, score, passed

Load into Pandas and run EDA checklist.

Calculate df.corr() and print correlation matrix.

Create seaborn heatmap (coolwarm, annotated).

Identify top 3 strongest and weakest correlations.

Plot scatter plots for 2 most correlated pairs with regression line.

Comment: Does more study always mean higher score?

Deliverables:

students.csv

heatmap.png

2 scatter plots

Written analysis

Bonus: sns.pairplot(hue='passed')

📑 Task 04: Full EDA Report (Capstone)
Goal: Perform a complete EDA on a real-world dataset from a public API.

Steps Implemented
Fetch dataset via API (sports, crypto, weather, books, etc.).

Clean data with Pandas ETL.

Run full EDA checklist (shape, nulls, describe, value_counts, distributions).

Create at least 5 charts:

Histogram

Box plot

Bar chart

Scatter plot

Correlation heatmap

Label all charts (title, xlabel, ylabel).

Save charts as .png.

Write 8–10 observations in comments or .txt.

Compare distributions between categories.

Bonus: sns.pairplot() to find most interesting relationship.

Deliverables:

.py script

5+ charts saved as .png

Written report (8–10 insights)
