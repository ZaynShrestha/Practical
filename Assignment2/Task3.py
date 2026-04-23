# #3. Use the open-Meteo weather API (free, no key needed) to fetch 7-day weather forecast for kathmandu. Save
# to CSV. Find the hottest and coldest.

# steps:
# API:https://api.open-meteo.com/v1/forecast
# Params: KTM's latitude, longitude, daily=temperature_2m_max
# Save:date + max_temp to weather.csv
# Find max/min temp and print which day
# Bonus: save a summary to a .txt File
# Deliverable: weather.csv + analysis script

import requests
import csv

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 27.7172,
    "longitude": 85.3240,
    "daily": "temperature_2m_max",
    "timezone": "auto"
}

# Step 1: Fetch data
response = requests.get(url, params=params)
data = response.json()

dates = data["daily"]["time"]
temps = data["daily"]["temperature_2m_max"]

# Step 2: Save to CSV
with open("weather.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["date", "max_temp"])

    for date, temp in zip(dates, temps):
        writer.writerow([date, temp])

print("Weather data saved")

# Step 3: Analysis
max_temp = max(temps)
min_temp = min(temps)

hottest_day = dates[temps.index(max_temp)]
coldest_day = dates[temps.index(min_temp)]

print(f"Hottest Day: {hottest_day} ({max_temp}°C)")
print(f"Coldest Day: {coldest_day} ({min_temp}°C)")

# Step 4: Save summary
with open("summary.txt", "w") as file:
    file.write(f"Hottest Day: {hottest_day} ({max_temp}°C)\n")
    file.write(f"Coldest Day: {coldest_day} ({min_temp}°C)\n")

print("Summary saved to summary.txt")