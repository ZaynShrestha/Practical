# Task 3:  Multi-Source ETL  [Hard]
# Merge data from two sources, clean and combine, load as one unified dataset
# Goal: Combine users and their posts from two API endpoints into one clean merged DataFrame.

# 1. EXTRACT: Fetch users from  /users  and posts from  /posts  — two separate API calls
# 2. Create two DataFrames:  df_users  and  df_posts
# 3. From df_users keep: id, name, email, city (from address.city — requires pd.json_normalize!)
# 4. From df_posts keep: userId, title — rename userId to  id  to match users
# 5. TRANSFORM: Merge the two DataFrames on  id  using  pd.merge(df_users, df_posts, on='id')
# 6. Count posts per user — add a  post_count  column to df_users using df_posts.groupby('id').size()
# 7. Clean: lowercase email, strip whitespace from name and city, drop nulls
# 8. LOAD: Save to  merged_data.csv  and  merged.db  — print the top 3 most active users

# Deliverable:  merged_data.csv  +  merged.db  +  top 3 users printed  ·  Bonus: also merge todos and add  completion_rate  column


import requests
import pandas as pd
import sqlite3

def fetch_data():
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    posts = requests.get("https://jsonplaceholder.typicode.com/posts").json()
    todos = requests.get("https://jsonplaceholder.typicode.com/todos").json()  # Bonus
    return users, posts, todos

def create_dataframes(users, posts, todos):
    # Normalize users
    df_users = pd.json_normalize(users)
    df_users = df_users[['id', 'name', 'email', 'address.city']]
    df_users.rename(columns={'address.city': 'city'}, inplace=True)

    # Posts
    df_posts = pd.DataFrame(posts)[['userId', 'title']]
    df_posts.rename(columns={'userId': 'id'}, inplace=True)

    # Todos (Bonus)
    df_todos = pd.DataFrame(todos)[['userId', 'completed']]
    df_todos.rename(columns={'userId': 'id'}, inplace=True)

    return df_users, df_posts, df_todos

def transform_data(df_users, df_posts, df_todos):
    # Merge users with posts
    merged = pd.merge(df_users, df_posts, on='id', how='left')

    # Post count per user
    post_counts = df_posts.groupby('id').size().reset_index(name='post_count')
    df_users = pd.merge(df_users, post_counts, on='id', how='left').fillna({'post_count': 0})

    # Bonus: completion rate from todos
    completion_rate = df_todos.groupby('id')['completed'].mean().reset_index(name='completion_rate')
    df_users = pd.merge(df_users, completion_rate, on='id', how='left')

    # Clean data
    df_users['email'] = df_users['email'].str.lower().str.strip()
    df_users['name'] = df_users['name'].str.strip()
    df_users['city'] = df_users['city'].str.strip()
    df_users.dropna(inplace=True)

    return merged, df_users

def load_data(merged, df_users):
    # Save to CSV
    merged.to_csv("merged_data.csv", index=False)

    # Save to SQLite
    conn = sqlite3.connect("merged.db")
    merged.to_sql("merged_data", conn, if_exists="replace", index=False)
    df_users.to_sql("users_summary", conn, if_exists="replace", index=False)
    conn.close()

    # Print top 3 most active users
    top_users = df_users.sort_values("post_count", ascending=False).head(3)
    print("\nTop 3 Most Active Users:")
    print(top_users[['id', 'name', 'email', 'city', 'post_count', 'completion_rate']])

def main():
    users, posts, todos = fetch_data()
    df_users, df_posts, df_todos = create_dataframes(users, posts, todos)
    merged, df_users = transform_data(df_users, df_posts, df_todos)
    load_data(merged, df_users)

if __name__ == "__main__":
    main()

