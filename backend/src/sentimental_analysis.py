from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyse(data_list):
    if not data_list:
        return 0.0
    
    analyzer = SentimentIntensityAnalyzer()
    total_compound_score = 0
    
    for text in data_list:
        score = analyzer.polarity_scores(text)['compound']
        total_compound_score += score

    #Calculate average
    avg_score = total_compound_score / len(data_list)
    return avg_score
