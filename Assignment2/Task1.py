#1. Use the JSONPlaceholder API to fetch a list of users. Print each user's name and email
#to the teminal.

# API:
# https://jsonplaceholder.typicode.com/users

# Steps:
# 1. Send GET request using requests
# 2. Check response status (200 OK)
# 3. Loop through data
# 4. Print name, email, and city

# Output:
# - Show user details in terminal
# - Take screenshot of output
# """

import requests

url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url)

    if response.status_code == 200:
        users = response.json()

        for user in users:
            name = user["name"]
            email = user["email"]
            city = user["address"]["city"]

            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"City: {city}")
            print("-" * 30)
    else:
        print("Failed to fetch data")

except Exception as e:
    print("Error:", e)