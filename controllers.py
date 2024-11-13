import psycopg2
from config import DATABASE

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DATABASE['dbname'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port']
        )
        print("Connected to database:", DATABASE['dbname'])
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_data():
    """Fetches data from the 'dashboard_data' table."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM dashboard_data"
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [
            'id', 'intensity', 'likelihood', 'relevance', 'year', 'country', 
            'topic', 'region', 'city', 'sector', 'pestle', 'source', 'swot'
        ]
        data = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        return data
    except psycopg2.Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        conn.close()
