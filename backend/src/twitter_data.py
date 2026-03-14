import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect('worldview_tweet.db')

# Write a SQL query to pull everything into a Pandas DataFrame
# (Change 'tweets' to whatever your table name is if it's different)
df = pd.read_sql_query("SELECT * FROM tweets", conn)

# Close the connection
conn.close()

# View the data
print(df.head()) # Shows the first 5 rows
print(f"\nTotal rows collected: {len(df)}")