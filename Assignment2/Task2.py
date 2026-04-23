#2. Fetch posts from the API. Save them a CSV with columns: id, title,body. Then read the CSV back and point
# only posts where title contains more than 5 words.

#Steps:
# - Endpoint:/posts
# - save:id, title, body to post.csv
#- Read back with DictReader
#- Filter: Posts having title more than 5 words and write in a new CSV
#- Deliverable: posts.csv + filter script + new csv

import requests
import csv

url = "https://jsonplaceholder.typicode.com/posts"

# Step 1: Fetch data
response = requests.get(url)
posts = response.json()

# Step 2: Save to CSV
with open("posts.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
    writer.writeheader()

    for post in posts:
        writer.writerow({
            "id": post["id"],
            "title": post["title"],
            "body": post["body"]
        })

print("Saved to posts.csv")

# Step 3: Read and filter
filtered_posts = []

with open("posts.csv", "r", encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        title_word_count = len(row["title"].split())

        if title_word_count > 5:
            filtered_posts.append(row)

# Step 4: Save filtered data
with open("filtered_posts.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "title", "body"])
    writer.writeheader()
    writer.writerows(filtered_posts)

print("Filtered data saved to filtered_posts.csv")