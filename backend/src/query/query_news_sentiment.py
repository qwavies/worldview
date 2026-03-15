import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your website to access this API

def get_news_db_connection():
    # This gets the absolute path to your 'Hackathon' folder
    # We go up 3 levels from 'backend/src/query/' to reach 'Hackathon/'
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    
    # Now we target the databases folder specifically
    db_path = os.path.join(base_dir, 'databases', 'worldview_news.db')
    
    # Print this to your terminal so you can verify it's correct!
    print(f"--- Attempting to open database at: {db_path} ---")
    
    if not os.path.exists(db_path):
        print("!!! ERROR: The file was not found at that path !!!")
        raise FileNotFoundError(f"Database not found at {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/sentiment/news', methods=['GET'])
def get_news_country_pairs():
    try:
        conn = get_news_db_connection('news_database.db')
        # Matches your NEWS table columns: source_country, target_country, sentiment_score
        query = """
        SELECT 
            source_country as country_a, 
            target_country as country_b, 
            AVG(sentiment_score) as avg_score, 
            COUNT(*) as mention_count
        FROM NEWS
        GROUP BY source_country, target_country
        ORDER BY avg_score DESC;
        """
        rows = conn.execute(query).fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)