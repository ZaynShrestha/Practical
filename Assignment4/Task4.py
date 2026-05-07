# ##Task4: Update, Delete & Data Integrity
# #Ques: Build a student grade management system — insert, update, delete, and validate data.
#1. Create grades.db with a students table: id, name, subject, score, grade TEXT
#2. Insert 15 students with various scores (mix them between 40–100)
#3. Write a function assign_grade(score) that returns A/B/C/D/F based on score
#4. UPDATE all rows — set the grade column using your function
#5. DELETE all students who scored below 50 — they didn't pass
#6. Add a new column passed BOOLEAN using ALTER TABLE — set it based on score >= 50
#7. Query: show count of students per grade, ordered from A to F
#8. Handle the case where a student name is entered twice — check before insertingimport sqlite3

import sqlite3

conn = sqlite3.connect("grades.db")
cursor = conn.cursor()

#Create Table:

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    score INTEGER,
    grade TEXT
)
""")

#Insert data (15 Students):

students_data = [
    ("Zayn", "Math", 95),
    ("Sama", "Science", 88),
    ("Shira", "English", 72),
    ("Biswass", "Math", 61),
    ("Suhana", "Science", 45),
    ("Suprina", "English", 55),
    ("Anita", "Math", 83),
    ("Sujan", "Science", 91),
    ("Dip", "English", 49),
    ("Rashi", "Math", 77),
    ("Samriddhi", "Science", 68),
    ("Swaroop", "English", 52),
    ("Bipin", "Math", 39),
    ("Harry", "Science", 84),
    ("Bhabishya", "English", 90)
]

#Duplicate check insert:

def insert_student(name, subject, score):
    cursor.execute("SELECT * FROM students WHERE name=?", (name,))
    exists = cursor.fetchone()

    if exists:
        print(f" Student {name} already exists. Skipping insert.")
    else:
        cursor.execute("""
            INSERT INTO students (name, subject, score)
            VALUES (?, ?, ?)
        """, (name, subject, score))

#Insert all students safely:

for s in students_data:
    insert_student(s[0], s[1], s[2])


conn.commit()

#Grade Function:

def assign_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
    
#Update grades:

cursor.execute("SELECT id, score FROM students")
rows = cursor.fetchall()

for row in rows:
    student_id = row[0]
    score = row[1]
    grade = assign_grade(score)

    cursor.execute("""
        UPDATE students
        SET grade = ?
        WHERE id = ?
    """, (grade, student_id))

conn.commit()

#Add Passed Column:


cursor.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cursor.fetchall()]

if "passed" not in columns:
    cursor.execute("ALTER TABLE students ADD COLUMN passed BOOLEAN")

#Set passed status:

cursor.execute("SELECT id, score FROM students")

for row in cursor.fetchall():
    passed = 1 if row[1] >= 50 else 0

    cursor.execute("""
        UPDATE students
        SET passed = ?
        WHERE id = ?
    """, (passed, row[0]))

conn.commit()

#Delete failed Students:

cursor.execute("DELETE FROM students WHERE score < 50")
conn.commit()

#Query FUnction:

def show(title, query):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

#query: Count per grade:

show(
    "Count of students per grade (A to F)",
    """
    SELECT grade, COUNT(*) AS total
    FROM students
    GROUP BY grade
    ORDER BY grade ASC
    """
)

#Final data check:

show(
    "Final Students Table",
    "SELECT * FROM students"
)

conn.close()

print("\n Grade management system completed successfully!")