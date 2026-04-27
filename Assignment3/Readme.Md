# 📰 News Data Pipeline & Analysis

This project implements a simple end-to-end data workflow using Python. It consists of two scripts:

- `data_pipeline.py` → Collects and stores news data from an API  
- `data_analysis.py` → Cleans, processes, and analyzes the collected data  

Together, they fetch, store, and generate insights from news headlines across multiple countries.

---

## 📦 Features

### 🔄 Data Pipeline
- Fetches news headlines from multiple countries:
  - Nepal np
  - India in
  - USA us
  - UK gb
  - Australia au
- Cleans and structures API response data  
- Stores data in a CSV file (`news_data.csv`)  
- Removes duplicate headlines based on:
  - Title  
  - Source  

---

### 📊 Data Analysis
- Computes:
  - Country with most headlines  
  - Average headline length per country  
  - Duplicate headlines across countries  
  - Most frequent news source  
  - Percentage of recent (<6 hours) vs older headlines  

- Filters:
  - Long headlines (>6 words) into a separate CSV  

- Identifies:
  - Country with longest average headlines  
  - Country with shortest average headlines  

---

## 🛠️ Tech Stack

- Python  
- Pandas  
- Requests  
- python-dotenv  

---

## 🚀 Usage

### Step 1: Run Data Pipeline
```bash
python data_pipeline.py
