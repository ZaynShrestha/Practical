# Store & API Monitor Projects

This repository contains two independent Python + MySQL projects:

1. **Store Database System** — a relational schema with customers, products, and orders, plus analytics queries and CSV export.
2. **API Monitor with Change Detection** — a monitoring pipeline that fetches posts from an API, detects changes between runs, and logs them.

---

## 📦 Task 1 · Store Database System

### Overview
- Database: `store_db`
- Tables: `customers`, `products`, `orders`
- Relationships: `orders` links to both `customers` and `products` via foreign keys
- Inserts: 10 customers, 8 products, 20 orders
- Queries:
  1. Total money spent per customer (JOIN + price × quantity, sorted highest first)
  2. Most ordered product by total quantity
  3. Customers who placed more than 2 orders (HAVING COUNT)
  4. Average order value per city
- Export: Revenue-per-customer results → `revenue_report.csv`

### How to Run
1. Ensure MySQL server is running and accessible.
2. Update connection credentials in the script (`user`, `password`).
3. Run the Python script:
   ```bash
   python store_db.py
Check the console for query outputs.

Verify revenue_report.csv is created in the project directory.

📡 Task 2 · API Monitor with Change Detection
Overview
Database: monitor_db

Tables:

posts: stores fetched API data

change_log: records what changed and when

API: JSONPlaceholder Posts

Behavior:

First run: inserts all posts, logs each as NEW

Subsequent runs: detects mismatches (e.g., after manual DB update) and logs as MODIFIED

Reports:

Post count per user

All change log entries from the latest run

User who triggered the most change events

Error handling: Every API call and DB operation wrapped in try/except with printed error messages

How to Run
Ensure MySQL server is running and accessible.

Update connection credentials in the script (user, password).

Run the Python script:

bash
python api_monitor.py
On first run, all posts are inserted and logged as NEW.

To simulate a change:

sql
UPDATE monitor_db.posts SET title='Changed' WHERE id=1;
Then rerun the script — the mismatch will be detected and logged as MODIFIED.

🛠 Requirements
Python 3.8+

MySQL server

Packages:

bash
pip install mysql-connector-python requests
📂 Deliverables
store_db.py — Store database system script

revenue_report.csv — Exported revenue report

api_monitor.py — API monitor script

README.md — Documentation

🚀 Notes
Both scripts are idempotent: tables are created if not existing, and inserts are safe to rerun.

Prices use DECIMAL(10,2) for accuracy.

Change detection compares both title and body fields.

Error handling ensures resilience against API or DB failures.

📊 Example Outputs
Total Money Spent Per Customer

Most Ordered Product

Customers with More Than 2 Orders

Average Order Value Per City

Post Count Per User

Latest Change Log Entries

User with Most Changes

📌 Author
Developed by Simran · Kathmandu, Nepal
