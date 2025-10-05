import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()


def insert_data_from_csv():
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()

        def process_companies():
            with open('scraped_data/raw/metadata/company_metadata.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cur.execute(
                        "INSERT INTO stock_data.companies (ticker, company_name, sector, industry, scrape_date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (ticker) DO NOTHING", row)

        def process_dividend_data():
            with open('scraped_data/raw/dividend_data/all_dividend_data.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cur.execute(
                        "INSERT INTO stock_data.dividend_data (ticker, date, dividend) VALUES (%s, %s, %s)", (row[2], row[0], row[1]))

        def process_stock_data():
            with open('scraped_data/raw/stock_data/all_stock_data.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cur.execute("INSERT INTO stock_data.stock_data (ticker, date, open, high, low, close, volume, dividends, stock_splits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                        row[7], row[8], row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        process_companies()
        process_dividend_data()
        process_stock_data()

        conn.commit()

    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Database error: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    insert_data_from_csv()
