import requests
import xml.etree.ElementTree as ET
import json
import datetime
import urllib.parse
import re

# Configuration
SCHEDULE_API_URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/16/schedule"
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCP0Cdc6moLMyDJiO0s-yhbQ"
OUTPUT_FILE = "insights.json"

def get_upcoming_game():
    """Fetches the next Bears game and its kickoff time."""
    try:
        response = requests.get(SCHEDULE_API_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        
        for event in data.get('events', []):
            game_date_str = event.get('date')
            if not game_date_str:
                continue
                
            game_date = datetime.datetime.strptime(game_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
            
            if game_date > now_utc - datetime.timedelta(hours=12):
                return {
                    "matchup": event.get('name', 'Chicago Bears'),
                    "kickoff": game_date_str # Keep ISO format for JavaScript countdown
                }
    except Exception as e:
        print(f"Schedule API error: {e}")
    return None

def get_news(matchup):
    """Pulls Google News RSS for the specific matchup."""
    news = []
    if not matchup:
        return news
        
    search_query = matchup.replace(' at ', ' ').replace(' vs. ', ' ').replace(' vs ', ' ')
    encoded = urllib.parse.quote_plus(search_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}+when:7d&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item')[:3]:
            title = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else "#"
            if title:
                news.append({
                    "headline": title.rsplit(' - ', 1)[0],
                    "link": link
                })
    except Exception as e:
        print(f"News RSS error: {e}")
    return news

def get_videos():
    """Pulls latest Official Bears YouTube videos and formats them for embedding."""
    videos = []
    try:
        response = requests.get(YOUTUBE_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
        
        for entry in root.findall('atom:entry', ns)[:2]: # Get top 2 videos
            title = entry.find('atom:title', ns).text
            video_id = entry.find('yt:videoId', ns).text
            if title and video_id:
                videos.append({
                    "title": title,
                    "embed_url": f"https://www.youtube.com/embed/{video_id}"
                })
    except Exception as e:
        print(f"YouTube RSS error: {e}")
    return videos

def build_dashboard():
    game_info = get_upcoming_game()
    matchup_name = game_info["matchup"] if game_info else None
    
    dashboard_data = {
        "game": game_info,
        "news": get_news(matchup_name),
        "videos": get_videos()
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(dashboard_data, f, indent=4)
    print("Dashboard JSON generated successfully.")

if __name__ == "__main__":
    build_dashboard()