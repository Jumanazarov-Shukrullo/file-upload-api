import psycopg2

from core.config import settings

conn = psycopg2.connect(settings.DATABASE_URL)
cursor = conn.cursor()

try:
    cursor.execute("""
    CREATE TABLE files (
    id VARCHAR PRIMARY KEY,
    filename VARCHAR NOT NULL,
    content_type VARCHAR NOT NULL,
    url VARCHAR NOT NULL,
    size INTEGER NOT NULL
);
""")
    conn.commit()
    print("Table created successfully!")

except Exception as e:
    print(f'occurred error: {e}')
finally:
    conn.close()