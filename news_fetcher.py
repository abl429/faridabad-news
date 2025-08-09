import requests
from bs4 import BeautifulSoup
import json
import time

def fetch_hindi_news():
    news_data = {"Hindi News": []}

    # Example 1: BBC Hindi
    try:
        url = "https://www.bbc.com/hindi"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("h2"):  # BBC headlines
            title = item.get_text(strip=True)
            if title and len(news_data["Hindi News"]) < 5:
                news_data["Hindi News"].append({
                    "title": title,
                    "content": "विस्तार से पढ़ने के लिए BBC Hindi देखें।"
                })
    except Exception as e:
        print("Error fetching BBC Hindi:", e)

    # Example 2: Aaj Tak
    try:
        url = "https://www.aajtak.in/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        for item in soup.select("h2"):  # Aaj Tak headlines
            title = item.get_text(strip=True)
            if title and len(news_data["Hindi News"]) < 10:
                news_data["Hindi News"].append({
                    "title": title,
                    "content": "Aaj Tak पर पूरी खबर देखें।"
                })
    except Exception as e:
        print("Error fetching Aaj Tak:", e)

    # Save to JSON file
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=4)

    print("News updated!")

if __name__ == "__main__":
    while True:
        fetch_hindi_news()
        time.sleep(600)  # 10 min
