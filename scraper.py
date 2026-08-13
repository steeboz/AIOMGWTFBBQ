import requests
from bs4 import BeautifulSoup
import json
import datetime

# Configuration
SEARCH_URL = "https://www.cbssports.com/nfl/players/3139822/caleb-williams/news/"
OUTPUT_FILE = "insights.json"

def scrape_insights():
    print(f"[{datetime.datetime.now()}] Initiating Caleb Williams Pregame Scrape...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        insights = []
        
        # This targets the news feed items on CBS Sports player pages (adjust class names if targeting a different site)
        news_items = soup.find_all('div', class_='ArticleList-articleText')
        
        for item in news_items[:3]: # Grab the top 3 most recent articles/blurbs
            title_tag = item.find('a')
            summary_tag = item.find('p')
            
            if title_tag and summary_tag:
                insights.append({
                    "date": datetime.datetime.now().strftime("%B %d, %Y"),
                    "headline": title_tag.text.strip(),
                    "summary": summary_tag.text.strip()
                })
                
        # Save scraped data to a JSON file so the HTML can read it
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(insights, f, indent=4)
            
        print(f"Successfully scraped {len(insights)} insights.")
        
    except Exception as e:
        print(f"An error occurred while scraping: {e}")

if __name__ == "__main__":
    scrape_insights()