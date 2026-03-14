import requests
from bs4 import BeautifulSoup 
import sqlite3

# Initialize VADER
def RedditScrapper(countryA, countryB):

    # Added a User-Agent to avoid getting blocked by Reddit
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    base_url = f"https://www.reddit.com/r/{countryA}/search/?q={countryB}&type=posts&t=month"

    session = requests.session()
    session.headers.update(headers)

    response = session.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('a', {'data-testid': 'post-title'})

    data = [] # Store dictionaries with text and sentiment

    for post in posts:
        relative_url = post.get('href')
        if not relative_url: continue
        
        json_url = f"https://www.reddit.com{relative_url.rstrip('/')}.json"
        
        post_response = session.get(json_url)
        
        if post_response.status_code == 200:
            json_data = post_response.json()
            
            #GET POST HEADER (Title) AND TEXT (Body)
            post_info = json_data[0]['data']['children'][0]['data']
            title = post_info.get('title', '')
            body = post_info.get('selftext', '')
            
            # Combine title and body for a full post analysis, or analyze separately
            post_content = f"{title} {body}".strip()
            
            if post_content:
                data.append(post_content)
            
            # GET COMMENTS
            comments = json_data[1]['data']['children']

            for comment in comments:
                if comment['kind'] == 't1':
                    comment_body = comment['data'].get('body', '')
                    data.append(comment_body)

    return countryA, countryB, data

if __name__ == "__main__":
    RedditScrapper(countryA="Australia", countryB="USA")

            

