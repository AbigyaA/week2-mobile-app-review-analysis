import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

conn = psycopg2.connect(
    dbname='bank_reviews',
    user='postgres',
    password='',
    host='localhost',
    port='5432'
)

df = pd.read_sql("""
    SELECT r.*, b.name as bank_name 
    FROM reviews r 
    JOIN banks b ON r.bank_id = b.bank_id;
""", conn)

conn.close()

print(df.head())
print(df.info())
print(df.describe())
print(df['source'].value_counts())
print(df['bank_name'].value_counts())
print(df.isnull().sum())

df = df.dropna(subset=['rating', 'review_text'])

plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='bank_name', order=df['bank_name'].value_counts().index)
plt.xticks(rotation=45)
plt.title("Number of Reviews per Bank")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df['rating'], bins=5, kde=True)
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.show()

avg_rating = df.groupby('bank_name')['rating'].mean().sort_values(ascending=False)
avg_rating.plot(kind='bar', figsize=(10, 5), title="Average Rating per Bank")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='rating', y='sentiment_score', hue='sentiment_label')
plt.title("Sentiment Score vs Rating")
plt.tight_layout()
plt.show()

print(df['theme'].value_counts())
