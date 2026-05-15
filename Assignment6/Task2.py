# Task 2:  API → Clean → Save  [Hard]
# Full ETL pipeline — real API data, Pandas clean, saved to CSV and SQLite
# Goal: Build a complete ETL pipeline from an API, clean the data with Pandas, and load to both CSV and SQLite.

# 1. EXTRACT: Fetch all 100 posts from  https://jsonplaceholder.typicode.com/posts
# 2. Load into a Pandas DataFrame using  pd.DataFrame(data)
# 3. TRANSFORM: Keep only columns  userId, id, title, body
# 4. Add a  word_count  column — count words in the title using .str.split().str.len()
# 5. Filter: keep only posts where word_count >= 4
# 6. Standardise: title to title case, strip whitespace from body
# 7. LOAD: Save cleaned data to  clean_posts.csv  (no index) and to SQLite  posts.db  using df.to_sql()
# 8. Print: total posts fetched, posts after filter, and top 3 users by post count

# Deliverable:  clean_posts.csv  +  posts.db  +  3 printed stats
# Bonus: Add error handling for the API call and validate that all userId values are integers


import pandas as pd
import requests
import sqlite3


url = "https://jsonplaceholder.typicode.com/posts"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # error handling for bad response
    data = response.json()
    print("API fetched successfully!")

except requests.exceptions.RequestException as e:
    print("API Error:", e)
    data = []


df = pd.DataFrame(data)

print("\nTotal posts fetched:", len(df))

df = df[["userId", "id", "title", "body"]]


# Validate userId is integer
df["userId"] = pd.to_numeric(df["userId"], errors="coerce").astype("Int64")

df["word_count"] = df["title"].str.split().str.len()

df_filtered = df[df["word_count"] >= 4]

print("Posts after filter:", len(df_filtered))


df_filtered["title"] = df_filtered["title"].str.title()
df_filtered["body"] = df_filtered["body"].str.strip()


df_filtered.to_csv("clean_posts.csv", index=False)
print("clean_posts.csv saved successfully!")

conn = sqlite3.connect("posts.db")

df_filtered.to_sql("posts", conn, if_exists="replace", index=False)

conn.close()

print("posts.db saved successfully!")


top_users = df_filtered["userId"].value_counts().head(3)

print("\nTop 3 users by post count:")
print(top_users)


print("\n========== SUMMARY ==========")
print("Total fetched posts :", len(df))
print("After filtering     :", len(df_filtered))
print("Files created       : clean_posts.csv, posts.db")