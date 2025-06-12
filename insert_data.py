import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

df = pd.read_csv("cleaned_reviews.csv")

df = pd.read_csv('cleaned_reviews.csv')

conn = psycopg2.connect(
    dbname='bank_reviews',
    user='postgres',
    password='iwamg', 
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
""")

# Create reviews table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    source VARCHAR(100),
    sentiment_label VARCHAR(50),
    sentiment_score NUMERIC,
    theme VARCHAR(100)
);
""")
conn.commit()

banks = df['bank'].unique()
bank_ids = {}
for bank in banks:
    cursor.execute("INSERT INTO banks (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING bank_id;", (bank,))
    result = cursor.fetchone()
    if result:
        bank_ids[bank] = result[0]
    else:
        cursor.execute("SELECT bank_id FROM banks WHERE name = %s;", (bank,))
        bank_ids[bank] = cursor.fetchone()[0]
conn.commit()

review_rows = []
for _, row in df.iterrows():
    review_rows.append((
        bank_ids[row['bank']],
        row.get('review_text', None),
        row.get('rating', None),
        row.get('review_date', None),
        row.get('source', None),
        row.get('sentiment_label', None),
        row.get('sentiment_score', None),
        row.get('theme', None)
    ))

execute_values(cursor, """
    INSERT INTO reviews (
        bank_id, review_text, rating, review_date, source, sentiment_label, sentiment_score, theme
    ) VALUES %s;
""", review_rows)
conn.commit()

cursor.close()
conn.close()
print("Data inserted successfully.")
