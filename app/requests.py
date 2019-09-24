import requests
from config import Config
from .models import Quotes
quotes_url = Config.QUOTES_URL
def getQuotes():
    random_quote = requests.get(quotes_url)
    new_quote = random_quote.json()
    author = new_quote.get("author")
    quote = new_quote.get("quote")
    permalink = new_quote.get("permalink")
    quote_object = Quotes(author,quote,permalink)
    return quote_object
