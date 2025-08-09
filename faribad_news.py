import threading
import time
import feedparser
from flask import Flask, render_template_string

app = Flask(__name__)

# Global storage for fetched news
news_data = {
    "english": [],
    "hindi": []
}

# HTML template for displaying news
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Faridabad News — Fatafat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
        header { background: #e63946; color: white; padding: 15px; text-align: center; font-size: 1.5em; }
        nav { background: #1d3557; padding: 10px; text-align: center; }
        nav a { color: white; margin: 0 15px; text-decoration: none; font-weight: bold; }
        .container { padding: 20px; }
        .news-block { background: white; margin-bottom: 15px; padding: 15px; border-radius: 5px; }
        .news-block h3 { margin: 0; }
        .news-block a { text-decoration: none; color: #1d3557; }
        .news-block a:hover { text-decoration: underline; }
        footer { text-align: center; padding: 15px; background: #e63946; color: white; }
    </style>
</head>
<body>
    <header>📰 Faridabad News — Fatafat</header>
    <nav>
        <a href="/">All</a>
        <a href="/english">English</a>
        <a href="/hindi">हिंदी</a>
    </nav>
    <div class="container">
        {% for category, articles in news.items() %}
            {% if show_all or category == filter_category %}
                <h2>{{ category.upper() }}</h2>
                {% for article in articles %}
                    <div class="news-block">
                        <h3><a href="{{ article.link }}" target="_blank">{{ article.title }}</a></h3>
                        <small>{{ article.published }}</small>
                    </div>
                {% endfor %}
            {% endif %}
        {% endfor %}
    </div>
    <footer>⚡ Fatafat News — Faridabad ⚡</footer>
</body>
</html>
"""

# Fetch news from RSS feeds
def fetch_news():
    global news_data
    feeds = {
        "english": [
            "https://news.google.com/rss/search?q=Faridabad&hl=en-IN&gl=IN&ceid=IN:en"
        ],
        "hindi": [
            "https://news.google.com/rss/search?q=Faridabad&hl=hi&gl=IN&ceid=IN:hi"
        ]
    }
    
    for category, urls in feeds.items():
        news_data[category] = []
        for url in urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                news_data[category].append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "No date")
                })

# Background thread to update news every 10 minutes
def background_updater():
    while True:
        fetch_news()
        time.sleep(600)  # 10 minutes

# Routes
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, news=news_data, show_all=True, filter_category=None)

@app.route("/english")
def english_news():
    return render_template_string(HTML_TEMPLATE, news=news_data, show_all=False, filter_category="english")

@app.route("/hindi")
def hindi_news():
    return render_template_string(HTML_TEMPLATE, news=news_data, show_all=False, filter_category="hindi")

if __name__ == "__main__":
    print("🚀 Starting Faridabad News backend...")
    fetch_news()
    threading.Thread(target=background_updater, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
