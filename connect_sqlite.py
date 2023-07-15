import sqlite3
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("SQlite db connected")
    except Exception as e:
        print(e)
    return conn

def run_query(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
    except Exception as e:
        print(e)