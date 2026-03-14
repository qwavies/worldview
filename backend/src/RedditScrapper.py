import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


country1 = "USA"
country2 = "CHINA"
base_url = f"https://www.reddit.com/r/{country1}/search/?q={country2}&type=posts&t=month"

session = requests.session()
response = session.get(base_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all('a', {'data-testid': 'post-title'})
data = []

for post in posts:
    relative_url = post.get('href')
    if not relative_url.endswith('.json'):
        json_url = f"https://www.reddit.com{relative_url.rstrip('/')}.json"
    
    post_response = session.get(json_url, verify=False)
    
    if post_response.status_code == 200:
        json_data = post_response.json()
        
        # --- GET POST TEXT ---
        post_info = json_data[0]['data']['children'][0]['data']
        post_text = post_info.get('selftext', '') # Main body text
        data.append(post_text)
        # --- GET COMMENTS ---
        comments = json_data[1]['data']['children']


        for comment in comments:
            if comment['kind'] == 't1':
                comment_body = comment['data'].get('body', '')
                if comment_body:
                    data.append(comment_body)
        
analyzer = SentimentIntensityAnalyzer()
results = []

for text in data:
    # Get the sentiment scores
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    
    # Categorize based on the compound score
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    results.append({
        "text": text,
        "compound_score": compound,
        "sentiment": sentiment
    })

