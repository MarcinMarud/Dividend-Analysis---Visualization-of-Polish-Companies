import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

queries_path = os.path.join(os.path.dirname(__file__), "..", "queries")

for filename in os.listdir(queries_path):
    if filename.endswith(".sql"):
        filepath = os.path.join(queries_path, filename)
        with open(filepath, "r") as f:
            query = f.read()
        view_name = os.path.splitext(filename)[0]
        cur.execute(sql.SQL("CREATE OR REPLACE VIEW stock_data.{view} AS {q}").format(
            view=sql.Identifier(view_name),
            q=sql.SQL(query)
        ))

conn.commit()
cur.close()
conn.close()
