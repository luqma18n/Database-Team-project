from psycopg2.extras import RealDictCursor
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn

if __name__ == '__main__':
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    create_sql = open('product_database/database/Create_Tables.sql', 'r')
    create_statement = create_sql.read()
    insert_sql = open('product_database/database/Dummy_Data.sql', 'r')
    insert_statement = insert_sql.read()
    cursor.execute(create_statement)
    cursor.execute(insert_statement)
    cursor.close()
    create_sql.close()
    insert_sql.close()
    conn.close()
else:
    print("Setup.py can only be run as a script.")