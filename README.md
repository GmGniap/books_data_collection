# books_data_collection
Collecting Authors + Books data as for Burmese literature records.

## Create SQLite db for data backup
- sql script to create table
```sql
create table books_data(book_id text,book_name text, book_price int, book_url text, book_header_name text, author_id text, author_name text, item_type text)
```

## PSL Data
- create old table
```python
sql_create_books_data = """
    CREATE TABLE IF NOT EXISTS books_data(
        id integer PRIMARY KEY,
        name text NOT NULL,
        description text,
        book_url text,
        price real,
        currency_code text,
        avg_rating real,
        image_url text,
        categories text,
        author_id integer,
        author_name text,
        author_slug text,
        pages text,
        size text,
        records text,
        is_purchasable numeric,
        is_in_stock numeric,
        remaining text
    )
"""
```
## List to do
- create requirements.txt for the required libraries
- another book site to scrape
