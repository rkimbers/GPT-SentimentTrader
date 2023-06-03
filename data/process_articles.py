# file: data/process_articles.py

def process_articles(raw_articles):
    # Here, you might want to clean the text, remove HTML tags, stop words, perform stemming, etc.

    processed_articles = []
    for article in raw_articles:
        text = article.get_text()  # extract text from the HTML of the article
        # perform additional processing here
        processed_articles.append(text)

    return processed_articles