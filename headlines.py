# Feed parser library
import feedparser
from  flask import Flask
headlines = Flask(__name__)

# BBC_FEED_URL = "http://feeds.bbci.co.uk/news/rss.xml"

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
 'cnn': 'http://rss.cnn.com/rss/edition.rss',
 'fox': 'http://feeds.foxnews.com/foxnews/latest',
 'iol': 'http://www.iol.co.za/cmlink/1.640'}

# Parse the BBC Rss feeds and use it
@headlines.route("/")
@headlines.route("/<publisher>")
def get_news(publisher='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publisher])
    first_article = feed['entries'][0]
    return """
        <html>
            <body>
                <b> {0} </b> <br/>
                <i> {1} </i>
                <p> {2} </p>
            </body>
        </html>
    """.format(first_article.get("title"),first_article.get("published"), first_article.get("summary"))


if __name__ == '__main__':
    headlines.run(port=5000, debug=True)
