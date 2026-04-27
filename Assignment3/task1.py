#1. You are given access to the GNews API (free tier at gnews.io). Build a complete automated data pipeline that answers the following questions: 
# # 1. Which country out of Nepal, India, USA, UK and Australia published the most headlines today? 
# # 2. What is the average number of words in a headline title — per country? 
# # 3. Are there any headlines that appeared in more than one country? If yes, which ones? 
# # 4. Which news source published the most headlines across all 5 countries combined? 
# # 5. What percentage of all headlines were published in the last 6 hours vs older than 6 hours? 
# # 6. If you run your script twice, does your database end up with duplicate rows? How did you prevent that? 
# # 7. Save only headlines with a title longer than 6 words to a CSV. How many passed that filter? 
# # 8. Which country had the longest headline on average — and which had the shortest? # Rules: 
# #9. All fetched data must be saved to a CSV file first — answer every question by reading from that CSV, not from the API response directly 
# # CSV must have clean column names — no spaces, all lowercase # If a field is missing from the API response, write "N/A" — never leave a cell empty 
# # Running the script twice must not create duplicate rows in the CSV 
# """ GNews Automated Data Pipeline =============================== Fetches top headlines from Nepal, India, USA, UK, Australia 
# Saves to CSV → answers 8 analysis questions from the CSV only Run twice → no duplicate rows (deduplication by title + url) """


import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timezone


load_dotenv()

API_KEY = os.getenv ("e2217411e918a90f25260ebe0af82044")

COUNTRIES = {
    "np": "Nepal",
    "in": "India",
    "us": "USA",
    "gb": "UK",
    "au": "Australia"
}

CSV_FILE = "all_news.csv"
FILTERED_CSV = "filtered_news.csv"


def fetch_and_save_data():
    all_articles = []

    for code, country_name in COUNTRIES.items():
        url = f"https://gnews.io/api/v4/top-headlines?country={code}&lang=en&max=10&token={API_KEY}"

        try:
            response = requests.get(url, timeout=10)

            print(f"\nFetching {country_name} -> Status:", response.status_code)

            if response.status_code != 200:
                print(response.text)
                continue

            data = response.json()

            for article in data.get("articles", []):
                all_articles.append({
                    "title": article.get("title") or "N/A",
                    "description": article.get("description") or "N/A",
                    "content": article.get("content") or "N/A",
                    "url": article.get("url") or "N/A",
                    "publishedat": article.get("publishedAt") or "N/A",
                    "sourcename": (article.get("source") or {}).get("name") or "N/A",
                    "country": country_name
                })

        except Exception as e:
            print(f"Error fetching {country_name}: {e}")

    df = pd.DataFrame(all_articles)

    if df.empty:
        print("\nNo data fetched.")
        return

    df.columns = df.columns.str.lower()

    df = df.fillna("N/A")

    if os.path.exists(CSV_FILE):
        old_df = pd.read_csv(CSV_FILE)
        df = pd.concat([old_df, df], ignore_index=True)

    df.drop_duplicates(subset=["url", "title"], inplace=True)

    df.to_csv(CSV_FILE, index=False)

    print(f"\nCSV saved -> {CSV_FILE}")


def analyze_data():
    if not os.path.exists(CSV_FILE):
        print("CSV not found. Run fetch first.")
        return

    df = pd.read_csv(CSV_FILE)
    df = df.fillna("N/A")

    df["word_count"] = df["title"].apply(lambda x: len(str(x).split()))

    print("\n===== ANALYSIS =====")

    print("\n1. Most headlines country:")
    print(df["country"].value_counts().idxmax())

    print("\n2. Avg words per country:")
    print(df.groupby("country")["word_count"].mean())

    print("\n3. Top source:")
    print(df["sourcename"].value_counts().head(1))

    filtered = df[df["word_count"] > 6]
    filtered.to_csv(FILTERED_CSV, index=False)

    print("\n7. Filtered rows:", len(filtered))


if __name__ == "__main__":
    fetch_and_save_data()
    analyze_data()