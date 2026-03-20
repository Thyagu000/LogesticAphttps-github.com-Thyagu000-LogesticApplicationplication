# db.py
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """
    Establishes and returns a PostgreSQL database connection
    using credentials from the .env file.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e

# Optional: Test connection if run directly
if __name__ == "__main__":
    conn = get_connection()
    print("Connected to PostgreSQL successfully!")
    conn.close()
