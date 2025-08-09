from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import threading
import time

app = Flask(__name__)

news_data = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>News Fatafat</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
        h1 { text-align: center; color: #d9534f; }
        .news-item { background: white; margin: 10px auto; padding: 15px; max-width: 800px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .source { font-size: 12px; color: gray; }
        .footer { text-align: center; padding: 20px; font-size: 20px; background-color: #d9534f; color: white; }
    </style>
</head>
<body>
    <h1>📰 News Fatafat</h1>
    {% for item in news %}
    <div class="news-item">
        <div class="source">{{ item['source'] }}</div>
        <h3>{{ item['title'] }}</h3>
        <p>{{ item['content'] }}</p>
    </div>
    {% endfor %}
    <div class="footer">⚡ Fatafat News ⚡</div>
</body>
</html>
"""

def fetch_news():
    global news_data
    news_data = []

    sources = [
        ("NDTV Hindi", "https://www.ndtv.com/hindi/latest", "h2 a"),
        ("Aaj Tak", "https://www.aajtak.in/india", "h2 a"),
        ("BBC Hindi", "https://www.bbc.com/hindi", "h3 a")
    ]

    for name, url, selector in sources:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")
            headlines = soup.select(selector)[:5]

            for h in headlines:
                title = h.get_text(strip=True)
                link = h.get("href")
                if not link.startswith("http"):
                    continue

                # Fetch article content
                try:
                    article_res = requests.get(link, timeout=10)
                    article_soup = BeautifulSoup(article_res.text, "lxml")
                    paragraphs = article_soup.find_all("p")
                    content = " ".join([p.get_text(strip=True) for p in paragraphs[:5]])
                except:
                    content = ""

                news_data.append({"source": name, "title": title, "content": content})
        except Exception as e:
            print(f"Error fetching from {name}: {e}")

def background_fetch():
    while True:
        print("Fetching latest news...")
        fetch_news()
        time.sleep(600)  # 10 minutes

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, news=news_data)

if __name__ == "__main__":
    threading.Thread(target=background_fetch, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
