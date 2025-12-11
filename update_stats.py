import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os
import sys

def fetch_stats():
    # URL for Caleb Williams' page on Pro-Football-Reference
    url = "https://www.pro-football-reference.com/players/W/WillCa03.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    content = ""

    # Attempt to fetch from URL
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text
        else:
            print(f"Failed to fetch URL: {response.status_code}")
    except Exception as e:
        print(f"Error fetching URL: {e}")

    # Fallback to local file if fetch failed (useful for dev/testing)
    if not content:
        local_file = 'caleb_stats.html'
        if os.path.exists(local_file):
            print(f"Using local file: {local_file}")
            with open(local_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            print("No content available (URL fetch failed and no local file).")
            return

    soup = BeautifulSoup(content, 'html.parser')

    # Use 'last5' table which actually contains all played games so far
    # In PFR, the "Game Logs" table on the main page often has id="last5"
    # even if it shows more than 5 games if it's the current season.
    table = soup.find('table', id='last5')

    if not table:
        print("Could not find Game Log table (id='last5').")
        return

    games = []
    season_stats = {
        "games_played": 0,
        "passing_yards": 0,
        "passing_tds": 0
    }

    # Iterate over rows
    rows = table.find('tbody').find_all('tr')

    for row in rows:
        if 'class' in row.attrs and 'thead' in row['class']:
            continue

        # Check if it's a valid game row
        date_cell = row.find('th', {'data-stat': 'date'}) # It's a th scope="row"
        if not date_cell:
            date_cell = row.find('td', {'data-stat': 'date'})

        if not date_cell:
            continue

        game_date_str = date_cell.text # e.g. "2025-12-07"

        # Determine if game is played
        result_cell = row.find('td', {'data-stat': 'game_result'})
        result_text = result_cell.text if result_cell else ""

        opp_cell = row.find('td', {'data-stat': 'opp_name_abbr'})
        opponent = opp_cell.text if opp_cell else "Unknown"

        loc_cell = row.find('td', {'data-stat': 'game_location'})
        is_away = loc_cell.text == '@' if loc_cell else False

        opp_display = f"{'@ ' if is_away else ''}{opponent}"

        played = False
        yards = 0
        tds = 0

        if result_text:
            played = True
            season_stats["games_played"] += 1

            yds_cell = row.find('td', {'data-stat': 'pass_yds'})
            if yds_cell and yds_cell.text:
                try:
                    yards = int(yds_cell.text)
                    season_stats["passing_yards"] += yards
                except ValueError:
                    pass

            td_cell = row.find('td', {'data-stat': 'pass_td'})
            if td_cell and td_cell.text:
                try:
                    tds = int(td_cell.text)
                    season_stats["passing_tds"] += tds
                except ValueError:
                    pass

        yt_query = f"Caleb Williams highlights vs {opponent} {game_date_str} 2025"
        yt_link = f"https://www.youtube.com/results?search_query={yt_query.replace(' ', '+')}"

        game_info = {
            "week": 0, # To be determined after sorting
            "date": game_date_str,
            "opponent": opp_display,
            "result": result_text,
            "played": played,
            "highlights_url": yt_link
        }

        games.append(game_info)

    # Sort games by date ascending
    games.sort(key=lambda x: x['date'])

    # Calculate weeks
    final_games = []

    if games:
        # Base date for Week 1 (Monday Sept 8, 2025)
        # Using a logic where Week 1 is around Sept 4-8.
        week_1_date = datetime.strptime("2025-09-08", "%Y-%m-%d")

        for game in games:
            try:
                g_date = datetime.strptime(game['date'], "%Y-%m-%d")
                # Calculate days difference from Week 1 start
                # Allowing for slight variations in schedule (Thursday/Sunday/Monday games)
                # Week 1 center is approx Sept 7.
                days_diff = (g_date - week_1_date).days

                # Formula: Week = round((days_diff) / 7) + 1
                week_num = round((days_diff) / 7) + 1
                if week_num < 1: week_num = 1 # Sanity check

                game['week'] = week_num
                final_games.append(game)
            except ValueError:
                # Handle invalid date format if any
                pass

    # Detect and insert Bye week if there's a gap
    if final_games:
        max_week = final_games[-1]['week']
        existing_weeks = {g['week'] for g in final_games}

        # Reconstruct list with Bye weeks
        filled_games = []
        for w in range(1, max_week + 1):
            if w in existing_weeks:
                # Find the game(s) for this week
                week_games = [g for g in final_games if g['week'] == w]
                filled_games.extend(week_games)
            else:
                filled_games.append({
                    "week": w,
                    "date": "BYE",
                    "opponent": "BYE",
                    "result": "",
                    "played": False,
                    "highlights_url": None
                })
        final_games = filled_games
        final_games.sort(key=lambda x: x['week'])

    output = {
        "stats": season_stats,
        "games": final_games,
        "updated_at": datetime.now().isoformat()
    }

    with open('stats.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Stats updated successfully. Found {len(final_games)} weeks/games.")

if __name__ == "__main__":
    fetch_stats()
