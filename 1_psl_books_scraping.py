from links import info
from connect_sqlite import create_connection, run_query

import requests
import re
import json
import sqlite3
from bs4 import BeautifulSoup

## Create sqlite database(if for the first time) and connect
db_file = "psl.db"

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
        pages integer,
        size text,
        records text,
        is_purchasable numeric,
        is_in_stock numeric,
        remaining text
    )
"""

conn = create_connection(db_file)
if conn is not None:
    run_query(conn, sql_create_books_data)

## Requesting book from API with specific index
info.change(5)
print(info.book_info_psl)
r = requests.get(info.book_info_psl)
print(r.status_code)

if r.status_code != 200:
    r.raise_for_status()

raw_data = r.json()

book_data = []
for index in range(len(raw_data)):
    book_info = raw_data[index]
    result = {}
    result["id"] = int(book_info["id"])
    result["name"] = book_info["name"]
    result["book_url"] = book_info["permalink"]

    ## to clean html tag from description
    raw_desp = BeautifulSoup(book_info["short_description"], "html.parser")
    result["description"] = raw_desp.text

    result["price"]= float(book_info["prices"]["price"])
    result["currency_code"]= book_info["prices"]["currency_code"]
    result["avg_rating"] = float(book_info["average_rating"])
    result["image_url"] = book_info["images"][0]["src"]
    result["categories"] = ",".join([str(book_info["categories"][i]["id"]) for i in range(len(book_info["categories"]))])
    result["author_id"] = book_info["tags"][0]["id"]
    result["author_name"] = book_info["tags"][0]["name"]
    result["author_slug"] = book_info["tags"][0]["slug"]
    result["pages"] = int(book_info["attributes"][0]["terms"][0]["name"])
    result["size"] = book_info["attributes"][1]["terms"][0]["name"]
    result["records"] = book_info["attributes"][2]["terms"][0]["name"]
    result["is_purchasable"] = bool(book_info["is_purchasable"])
    result["is_in_stock"] = bool(book_info["is_in_stock"])
    result["remaining"] = book_info["low_stock_remaining"]
    book_data.append(result)


