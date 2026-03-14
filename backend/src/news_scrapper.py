from newsapi import NewsApiClient

API = "b1845c151a194d6bbf1a8c6f15f332b6"
newsapi = NewsApiClient(api_key=API)
countryA = "USA"
countryB = "CHINA"
articles = newsapi.get_everything(
    q='China AND (opinion OR relations OR trade)',
    # Using 'domains' or searching specific Country A sources is often 
    # more effective than the general 'country' tag for opinions.
    language='en',
    sort_by='relevancy',
    verify = False)
print(articles)