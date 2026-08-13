import requests
import xml.etree.ElementTree as ET
import json
import datetime
import urllib.parse

# Configuration
SCHEDULE_API_URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/16/schedule"
# The official Chicago Bears YouTube Channel ID 
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCP0Cdc6moLMyDJiO0s-yhbQ"
OUTPUT_FILE = "insights.json"

def get_upcoming_matchup():
    """Fetches the Bears schedule to determine if we are in Game Week or Offseason/Camp."""
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
            
            # Find the first future game
            if game_date > now_utc - datetime.timedelta(hours=12):
                days_until = (game_date - now_utc).days
                matchup_string = event.get('name', 'Chicago Bears')
                
                # Only pull matchup news if the game is happening within 7 days
                if days_until <= 7:
                    search_query = matchup_string.replace(' at ', ' ').replace(' vs. ', ' ').replace(' vs ', ' ')
                    return search_query
                else:
                    print(f"Next game is {days_until} days away. Entering Offseason/Camp mode...")
                    return None
                    
        return None
    except Exception as e:
        print(f"Error fetching schedule from ESPN: {e}")
        return None

def fetch_youtube_updates():
    """Pulls the latest videos, live streams, and press conferences from the Official Bears YouTube channel."""
    print("Fetching latest from Official Chicago Bears YouTube...")
    insights = []
    
    try:
        response = requests.get(YOUTUBE_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        # YouTube RSS uses the Atom XML format
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
        
        # Grab the 3 most recent videos/streams
        for entry in root.findall('atom:entry', ns)[:3]:
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:link', ns).attrib['href']
            pub_date_str = entry.find('atom:published', ns).text
            
            try:
                parsed_date = datetime.datetime.strptime(pub_date_str, "%Y-%m-%dT%H:%M:%S%z")
                display_date = parsed_date.strftime("%B %d, %Y")
            except:
                display_date = datetime.datetime.now().strftime("%B %d, %Y")
            
            # Format a nice clickable HTML link based on the content type
            title_lower = title.lower()
            link_html = f"<a href='{link}' target='_blank' style='color: var(--bears-orange); text-decoration: none; font-weight: bold;'>▶ Watch Here</a>"
            
            if "press conference" in title_lower:
                summary = f"🎙️ New Press Conference available. {link_html}"
            elif "live" in title_lower:
                summary = f"🔴 Live stream broadcast. Tune in now: {link_html}"
            elif "camp" in title_lower:
                summary = f"🏈 Training Camp update. {link_html}"
            else:
                summary = f"📺 Latest video from the Chicago Bears Network. {link_html}"
                
            insights.append({
                "date": display_date,
                "headline": title,
                "summary": summary
            })
            
    except Exception as e:
        print(f"Error fetching YouTube RSS: {e}")
        
    return insights

def scrape_insights():
    matchup_query = get_upcoming_matchup()
    insights = []
    
    # 1. If we are in Game Week, try to find Matchup News
    if matchup_query:
        encoded_query = urllib.parse.quote_plus(matchup_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:7d&hl=en-US&gl=US&ceid=US:en"
        print(f"[{datetime.datetime.now()}] Initiating Game Week Scrape...")
        
        try:
            response = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ""
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                try:
                    parsed_date = datetime.datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                    display_date = parsed_date.strftime("%B %d, %Y")
                except:
                    display_date = datetime.datetime.now().strftime("%B %d, %Y")
                    
                if title:
                    clean_title = title.rsplit(' - ', 1)[0]
                    insights.append({
                        "date": display_date,
                        "headline": clean_title,
                        "summary": "Matchup analysis and latest updates ahead of the game."
                    })
                
                if len(insights) >= 3:
                    break
        except Exception as e:
            print(f"Google News RSS error: {e}")
            
    # 2. FALLBACK: If game is > 7 days away OR Google News returned 0 articles
    if len(insights) == 0:
        insights = fetch_youtube_updates()
        
    # 3. Save the results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(insights, f, indent=4)
        
    print(f"Successfully saved {len(insights)} insights.")

if __name__ == "__main__":
    scrape_insights()