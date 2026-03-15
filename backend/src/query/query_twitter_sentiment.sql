import sqlite3
import pandas as pd

conn = sqlite3.connect('worldview_tweet.db')

query = """
SELECT
    source_country, 
    target_country, 
    AVG(score) AS avg_score,
    count(*) over () as total_count
FROM tweets
WHERE score != 0
GROUP BY source_country, target_country;
"""

df_summary = pd.read_sql_query(query, conn)

conn.close()

print(df_summary)
