# Module 1 - Data Pipeline

This module collects book data from Books to Scrape, cleans the data,
converts prices from GBP to INR, and stores the results in SQLite.

## What I did

- Scraped books from 3 categories using `requests` and `BeautifulSoup`.
- Cleaned price, rating, and availability fields.
- Used the fixed rate **1 GBP = 105.50 INR**.
- Created `categories` and `books` tables with a foreign-key relationship.
- Ran SQL queries and saved their outputs.
- Used pandas to check the SQL results.

## Files

- `data_pipeline.ipynb` - complete pipeline
- `books.db` - SQLite database
- `queries.sql` - SQL queries
- `query_outputs.txt` - query results

## How to run

Install the required packages:

```bash
pip install requests beautifulsoup4 pandas