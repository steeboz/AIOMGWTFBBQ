import requests
import xml.etree.ElementTree as ET
import json
import datetime
import urllib.parse

# Configuration
# The ESPN API ID for the Chicago Bears is 16
SCHEDULE_API_URL = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/16/schedule"
OUTPUT_FILE = "insights.json"

def get_upcoming_matchup():
    """Fetches the Bears schedule from ESPN and returns the teams playing in the next game."""
    try:
        print("Checking ESPN API for the upcoming Chicago Bears schedule...")
        response = requests.get(SCHEDULE_API_URL, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        
        # GitHub Actions run in UTC, so we compare against current UTC time
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        
        for event in data.get('events', []):
            game_date_str = event.get('date')
            if not game_date_str:
                continue
                
            # ESPN returns dates in ISO format: "2026-08-15T17:00:00Z"
            game_date = datetime.datetime.strptime(game_date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
            
            # Find the first game that is in the future (or recently finished within the last 12 hours)
            if game_date > now_utc - datetime.timedelta(hours=12):
                # The 'name' field usually looks like "Cleveland Browns at Chicago Bears"
                matchup_string = event.get('name', 'Chicago Bears')
                print(f"--> Found upcoming matchup: {matchup_string} (Scheduled for {game_date.strftime('%B %d, %Y')})")
                
                # Replace ' at ' or ' vs ' with a space so Google News searches it as a broad keyword block
                search_query = matchup_string.replace(' at ', ' ').replace(' vs. ', ' ').replace(' vs ', ' ')
                return search_query
                
        print("--> No upcoming future games found in the current schedule.")
        return "Chicago Bears" # Fallback if season is over
        
    except Exception as e:
        print(f"Error fetching schedule from ESPN: {e}")
        return "Chicago Bears" # Fallback

def scrape_insights():
    # 1. Dynamically figure out who the Bears are playing this week
    matchup_query = get_upcoming_matchup()
    
    # 2. URL encode the matchup string (e.g., changes spaces to '+')
    encoded_query = urllib.parse.quote_plus(matchup_query)
    
    # 3. Build the Google News RSS URL with the dynamic query
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}+when:7d&hl=en-US&gl=US&ceid=US:en"
    
    print(f"[{datetime.datetime.now()}] Initiating RSS Scrape...")
    print(f"Querying Google News RSS: {rss_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(rss_url, headers=headers)
        response.raise_for_status()
        
        # Parse the XML from the RSS feed
        root = ET.fromstring(response.content)
        
        insights = []
        
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            # Format the publication date nicely
            try:
                parsed_date = datetime.datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                display_date = parsed_date.strftime("%B %d, %Y")
            except:
                display_date = datetime.datetime.now().strftime("%B %d, %Y")
                
            if title:
                # Remove the publisher name (e.g., " - ESPN") from the end of the headline
                clean_title = title.rsplit(' - ', 1)[0]
                
                insights.append({
                    "date": display_date,
                    "headline": clean_title,
                    "summary": f"Latest updates and news coverage for the upcoming {matchup_query} matchup."
                })
            
            # Stop once we have 3 good insights
            if len(insights) >= 3:
                break
                
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(insights, f, indent=4)
            
        print(f"Successfully scraped {len(insights)} dynamic insights.")
        
    except Exception as e:
        print(f"An error occurred while scraping: {e}")

if __name__ == "__main__":
    scrape_insights()