from newsapi import NewsApiClient
from deep_translator import GoogleTranslator
import pycountry
from dotenv import load_dotenv
import os

def news_scrapper(countryA, countryB):
    load_dotenv()
    newsapi = NewsApiClient(api_key=os.getenv('news_api'))
    
    #Map country names to NewsAPI-supported language codes
    #NewsAPI supports these specific 14 languages
    supported_langs = {
        'AR': 'ar', 'DE': 'de', 'EN': 'en', 'ES': 'es', 'FR': 'fr', 
        'HE': 'he', 'IT': 'it', 'NL': 'nl', 'NO': 'no', 'PT': 'pt', 
        'RU': 'ru', 'SE': 'se', 'ZH': 'zh', 'JP': 'jp'
    }

    try:
        countryA_info = pycountry.countries.search_fuzzy(countryA)[0]
        countryA_code = countryA_info.alpha_2.upper()
        
        # Determine the language to search in
        search_lang = supported_langs.get(countryA_code, 'en') # Default to English if not supported
        
        #Translate Country B's name into Country A's language
        translated_query = GoogleTranslator(source='auto', target=search_lang).translate(countryB)
        
        response = newsapi.get_everything(
            q=translated_query,
            language=search_lang,
            sort_by='relevancy',
            page_size=100
        )
        
        articles = response.get('articles', [])
        
        #Extract and Clean
        raw_titles = [
            a['title'].strip() 
            for a in articles 
            if a.get('title') and a['title'] != '[Removed]'
        ]
        
        if not raw_titles:
            return [f"No results found in {countryA} for '{countryB}'."]

        #Translate back to English
        #If the search_lang was already 'en', we skip the second translation
        if search_lang == 'en':
            return raw_titles
            
        translated_headlines = GoogleTranslator(source=search_lang, target='en').translate_batch(raw_titles)
        return translated_headlines

    except Exception as e:
        return [f"Error: {e}"]
    
print(news_scrapper("china", "USA"))