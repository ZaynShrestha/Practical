# Task 1 · Multi-Table Relational System [Hard]

# Using mysql-connector-python, create a database called store_db with three tables — customers, products, 
# and orders — where orders links to the other two via foreign keys. Insert at least 10 customers, 8 products, 
# and 20 orders using %s parameterized queries. Then run these 4 queries and print the results with clear labels: total money spent per customer 
# (JOIN + price × quantity, sorted highest first), most ordered product by total quantity, customers who placed more than 2 
# orders (HAVING COUNT), and average order value per city. Finally, export the revenue-per-customer result into a 
# revenue_report.csv using Python's csv module.

# Deliverable: MySQL store_db + Python script + revenue_report.csv


import mysql.connector
import csv

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@#$#1"
)

cursor = conn.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS store_db")
cursor.execute("USE store_db")

# Drop tables if they exist (to avoid duplicates on rerun)
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS products")

# Create Tables
cursor.execute("""
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    city VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2)
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# Insert Customers
customers = [
    ("Aarav", "Kathmandu"),
    ("Sita", "Lalitpur"),
    ("Ram", "Bhaktapur"),
    ("Gita", "Kathmandu"),
    ("Hari", "Pokhara"),
    ("Nabin", "Butwal"),
    ("Kiran", "Kathmandu"),
    ("Sujan", "Lalitpur"),
    ("Anita", "Pokhara"),
    ("Pratik", "Chitwan")
]
cursor.executemany("INSERT INTO customers (name, city) VALUES (%s, %s)", customers)

# Insert Products
products = [
    ("Laptop", 80000),
    ("Phone", 40000),
    ("Headphones", 3000),
    ("Mouse", 1200),
    ("Keyboard", 2500),
    ("Monitor", 20000),
    ("Tablet", 35000),
    ("Speaker", 5000)
]
cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s)", products)

conn.commit()

# Insert Orders (20)
orders = [
    (1, 1, 2), (1, 2, 1), (2, 3, 5),
    (3, 4, 2), (4, 5, 1), (5, 6, 3),
    (6, 7, 2), (7, 8, 1), (8, 1, 4),
    (9, 2, 2), (10, 3, 1), (1, 4, 2),
    (2, 5, 1), (3, 6, 3), (4, 7, 2),
    (5, 8, 1), (6, 1, 2), (7, 2, 3),
    (8, 3, 1), (9, 4, 2)
]

cursor.executemany("""
INSERT INTO orders (customer_id, product_id, quantity, order_date)
VALUES (%s, %s, %s, CURDATE())
""", orders)

conn.commit()

# Helper function to show results
def show(title, query):
    print("\n" + "="*60)
    print(title)
    print("="*60)
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

# 1. Total spent per customer

query1 = """
SELECT c.name,
       SUM(p.price * o.quantity) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
GROUP BY c.name
ORDER BY total_spent DESC
"""
show("Total Money Spent Per Customer", query1)

# 2. Most ordered product

query2 = """
SELECT p.name,
       SUM(o.quantity) AS total_qty
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY p.name
ORDER BY total_qty DESC
LIMIT 1
"""
show("Most Ordered Product", query2)

# 3. Customers with more than 2 orders

query3 = """
SELECT c.name,
       COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name
HAVING COUNT(o.order_id) > 2
"""
show("Customers with More Than 2 Orders", query3)

# 4. Average order value per city

query4 = """
SELECT c.city,
       AVG(p.price * o.quantity) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
GROUP BY c.city
"""
show("Average Order Value Per City", query4)

# Export revenue report to CSV

cursor.execute(query1)
revenue_data = cursor.fetchall()

with open("revenue_report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Customer Name", "Total Spent"])
    for row in revenue_data:
        writer.writerow(row)

print("\nrevenue_report.csv created successfully!")
conn.close()
print("\nSTORE DATABASE PROJECT COMPLETED!")
