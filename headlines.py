# Feed parser library
import feedparser
from  flask import Flask
from  flask import render_template
from  flask import request
headlines = Flask(__name__)

# BBC_FEED_URL = "http://feeds.bbci.co.uk/news/rss.xml"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
 'cnn': 'http://rss.cnn.com/rss/edition.rss',
 'fox': 'http://feeds.foxnews.com/foxnews/latest',
 'iol': 'http://www.iol.co.za/cmlink/1.640'}

# Parse the BBC Rss feeds and use it
@headlines.route("/",methods=['GET','POST'])
def get_news():
    # query = request.args.get("publisher")
    query = request.form.get("publisher")
    if not query or query.lower() not in RSS_FEEDS:
            publisher  = "bbc"
    else:
            publisher = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publisher])
    return render_template("home.html",
                            articles=feed['entries'])
if __name__ == '__main__':
    headlines.run(port=5000, debug=True)
