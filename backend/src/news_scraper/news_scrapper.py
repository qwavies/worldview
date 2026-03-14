from newsapi import NewsApiClient
from deep_translator import GoogleTranslator
import pycountry
from dotenv import load_dotenv
import os

def news_scrapper(countryA, countryB):
    load_dotenv()
    newsapi = NewsApiClient(api_key=os.getenv('news_api'))
    
    supported_langs = {
        'AR': 'ar', 'DE': 'de', 'EN': 'en', 'ES': 'es', 'FR': 'fr', 
        'HE': 'he', 'IT': 'it', 'NL': 'nl', 'NO': 'no', 'PT': 'pt', 
        'RU': 'ru', 'SE': 'se', 'ZH': 'zh', 'JP': 'jp'
    }

    try:
        #Get Country A Info
        countryA_info = pycountry.countries.search_fuzzy(countryA)[0]
        countryA_code = countryA_info.alpha_2.upper()
        search_lang = supported_langs.get(countryA_code, 'en')

        #translate both 
        trans_A = GoogleTranslator(source='auto', target=search_lang).translate(countryA)
        trans_B = GoogleTranslator(source='auto', target=search_lang).translate(countryB)
        
        #query
        query = f'+"{trans_A}" +"{trans_B}"'
        
        response = newsapi.get_everything(
            qintitle=query,
            language=search_lang,
            sort_by='relevancy',
            page_size=100
        )

        articles = response.get('articles', [])
        
        raw_titles = [
            a['title'].strip() 
            for a in articles 
            if a.get('title') and a['title'] != '[Removed]'
        ]
        
        if not raw_titles:
            return [f"No results found in {countryA} regarding {countryB}."]

        if search_lang == 'en':
            return raw_titles
            
        return GoogleTranslator(source=search_lang, target='en').translate_batch(raw_titles)

    except Exception as e:
        return [f"Error: {e}"]
    
print(news_scrapper("china", "USA"))