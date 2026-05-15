# #Clean a messy CSV
# Goal : Create a messy CSV yourself, then write a cleaning script that fixes every problem.
# 1. Create  messy_students.csv  manually — add at least 15 rows with these problems deliberately:
# → Some rows with missing score or name  → Duplicate rows  → Names in inconsistent casing
# → Score stored as string e.g. '85'  → Extra spaces in names  → Some scores below 0 (invalid)
# 2. Load it with Pandas and print df.info() + df.isnull().sum() — show the problems first
# 3. Fix all 6 problems: nulls, duplicates, casing, type, whitespace, invalid values
# 4. Add a  grade  column: A (≥90), B (≥75), C (≥50), F (<50) — use df['score'].apply()
# 5. Save the cleaned result to  clean_students.csv  and print a before/after row count

# Deliverable:  messy_students.csv  +  clean_students.csv  +  cleaning script
# Bonus: Print a full cleaning report — how many nulls, dupes, and bad values were fixed


import pandas as pd
import numpy as np

data = [
    ["zayn ", "85"],
    ["SAMA", "92"],
    ["shira", None],
    ["Biswass", "-10"],
    [None, "78"],
    ["Anita", "55"],
    ["sujan ", "40"],
    ["Rashi", "101"],
    [" zayn ", "85"],
    ["SAMA", "92"],
    ["Rohan", "67"],
    ["ram", "-5"],
    ["Hari ", "49"],
    ["sita", "88"],
    ["KIRAN", None],
    ["anita", "55"],
    ["ROHAN", "67"]
]

# IMPORTANT: add column names
df = pd.DataFrame(data, columns=["name", "score"])

# Add duplicate rows
df = pd.concat([df, df.iloc[[1, 3]]], ignore_index=True)

# Save messy CSV
df.to_csv("messy_students.csv", index=False)

print("messy_students.csv created successfully!")


df = pd.read_csv("messy_students.csv")

print("\n=MESSY DATA\n")
print(df)

print("\nDATA INFO\n")
print(df.info())

print("\nNULL VALUES\n")

print(df.isnull().sum())



before_rows = len(df)

null_names_before = df['name'].isnull().sum()
null_scores_before = df['score'].isnull().sum()
duplicates_before = df.duplicated().sum()

# Fix missing names
df['name'] = df['name'].fillna("Unknown")

# Convert score to numeric
df['score'] = pd.to_numeric(df['score'], errors='coerce')

# Fill missing scores
average_score = df['score'].mean()
df['score'] = df['score'].fillna(average_score)

# Remove spaces + fix casing
df['name'] = df['name'].str.strip()
df['name'] = df['name'].str.title()

# Fix invalid scores
invalid_scores_before = (df['score'] < 0).sum()
df.loc[df['score'] < 0, 'score'] = 0
df.loc[df['score'] > 100, 'score'] = 100

# Remove duplicates
df = df.drop_duplicates()


def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"

df['grade'] = df['score'].apply(grade)


df.to_csv("clean_students.csv", index=False)

print("\nclean_students.csv saved successfully!")

after_rows = len(df)

print("\nROW COUNT")
print("Before Cleaning:", before_rows)
print("After Cleaning :", after_rows)

print("\nCLEANING REPORT")
print("Missing Names Fixed     :", null_names_before)
print("Missing Scores Fixed    :", null_scores_before)
print("Duplicate Rows Removed  :", duplicates_before)
print("Invalid Scores Fixed    :", invalid_scores_before)

print("\nCLEANED DATA")
print(df)