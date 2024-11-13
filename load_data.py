import json
import psycopg2
from datetime import datetime
from config import DATABASE

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=DATABASE['dbname'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        port=DATABASE['port']
    )
    return conn

def load_json_data():
    """Load JSON data from a file with UTF-8 encoding."""
    try:
        with open('jsondata.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError as e:
        print("Error decoding JSON file:", e)
        return None

def parse_timestamp(date_str):
    """Convert a date string to a PostgreSQL-compatible timestamp."""
    try:
        return datetime.strptime(date_str, '%B, %d %Y %H:%M:%S')
    except ValueError:
        return None

def insert_data_to_db(data):
    """Insert JSON data into the PostgreSQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO dashboard_data (
            end_year, intensity, sector, topic, insight, url, region, start_year,
            impact, added, published, country, relevance, pestle, source, title, likelihood
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for entry in data:
        # Convert empty strings to None (NULL in PostgreSQL)
        end_year = entry.get('end_year') if entry.get('end_year') else None
        intensity = int(entry.get('intensity')) if entry.get('intensity') not in (None, '') else None
        sector = entry.get('sector') if entry.get('sector') else None
        topic = entry.get('topic') if entry.get('topic') else None
        insight = entry.get('insight') if entry.get('insight') else None
        url = entry.get('url') if entry.get('url') else None
        region = entry.get('region') if entry.get('region') else None
        start_year = entry.get('start_year') if entry.get('start_year') else None
        impact = entry.get('impact') if entry.get('impact') else None
        added = parse_timestamp(entry.get('added')) if entry.get('added') else None
        published = parse_timestamp(entry.get('published')) if entry.get('published') else None
        country = entry.get('country') if entry.get('country') else None
        relevance = int(entry.get('relevance')) if entry.get('relevance') not in (None, '') else None
        pestle = entry.get('pestle') if entry.get('pestle') else None
        source = entry.get('source') if entry.get('source') else None
        title = entry.get('title') if entry.get('title') else None
        likelihood = int(entry.get('likelihood')) if entry.get('likelihood') not in (None, '') else None

        # Insert the data into the database
        cursor.execute(insert_query, (
            end_year, intensity, sector, topic, insight, url, region, start_year,
            impact, added, published, country, relevance, pestle, source, title, likelihood
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded successfully!")

if __name__ == '__main__':
    try:
        data = load_json_data()
        insert_data_to_db(data)
    except Exception as e:
        print("Error loading data:", e)
