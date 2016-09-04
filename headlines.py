# Non Flask imports
import feedparser
import json
import urllib2
import urllib

# Cookies Support import
import datetime

# Flask imports
from  flask import Flask
from  flask import render_template
from  flask import request
from  flask import make_response

# Logic
headlines = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {  'publisher' : 'bbc',
               'city'     : 'Chennai,IN'
           }
# Parse the BBC Rss feeds and use it
@headlines.route("/",methods=['GET','POST'])
def home():
    # Prepare input for news
    query = request.form.get("publisher")
    if not query or query.lower() not in RSS_FEEDS:
            publisher = request.cookies.get("publisher")
            if not publisher:
                publisher  = DEFAULTS['publisher']
    else:
            publisher = query.lower()
    articles = get_news(publisher)

    # Prepare input for weather
    city = request.form.get("city")
    if not city:
        city = request.cookies.get("city")
        if not city:
            city = DEFAULTS['city']
    weather = get_weather(city)
    # return render_template("home.html",
                            # articles= articles,
                            # weather = weather )
    # Response object
    response = make_response(render_template("home.html",
                                             articles= articles,
                                             weather = weather
                                            )
                            )
    # Expiration period calculation
    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    # Prepare cookies to be set
    response.set_cookie("publisher",publisher,expires = expires)
    response.set_cookie("city",city,expires = expires)
    return response

def get_news(publisher):
    feed = feedparser.parse(RSS_FEEDS[publisher])
    return feed['entries']

def get_weather(query):
    api_url =  "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=08f5ff999981eee8f66e01f7e31bef6b"
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)

    if parsed.get("weather"):
        weather = { "description":parsed["weather"][0]["description"],
                    "temperature":parsed["main"]["temp"],
                    "city":parsed["name"],
                    'country': parsed['sys']['country']
                  }
    return weather

if __name__ == '__main__':
    headlines.run(port=5000, debug=True)
