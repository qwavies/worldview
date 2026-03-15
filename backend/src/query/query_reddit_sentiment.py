import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your website to access this API

def get_reddit_db_connection():
    # This gets the absolute path to your 'Hackathon' folder
    # We go up 3 levels from 'backend/src/query/' to reach 'Hackathon/'
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
    
    # Now we target the databases folder specifically
    db_path = os.path.join(base_dir, 'databases', 'worldview_reddit.db')
    
    # Print this to your terminal so you can verify it's correct!
    print(f"--- Attempting to open database at: {db_path} ---")
    
    if not os.path.exists(db_path):
        print("!!! ERROR: The file was not found at that path !!!")
        raise FileNotFoundError(f"Database not found at {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/sentiment/pairs', methods=['GET'])
def get_reddit_country_pairs():
    try:
        conn = get_reddit_db_connection()
        
        # This query pulls all country pairs and calculates the average score
        query = """
        SELECT 
            country_a, 
            country_b, 
            AVG(score) as avg_score, 
            COUNT(*) as mention_count
        FROM sentiment_results
        GROUP BY country_a, country_b
        ORDER BY avg_score DESC;
        """
        
        rows = conn.execute(query).fetchall()
        conn.close()

        # Convert the SQL rows into a list of dictionaries for JSON
        data = [dict(row) for row in rows]
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Runs the server on http://127.0.0.1:5000
    app.run(debug=True, port=5000)