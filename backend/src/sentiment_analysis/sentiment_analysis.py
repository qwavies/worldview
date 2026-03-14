from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(content: str) -> float:
    if not content:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(content)['compound']
