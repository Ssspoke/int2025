import requests
from bs4 import BeautifulSoup, Tag
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

URL = "https://liquipedia.net/dota2/The_International/2025/Main_Event"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

class LiquipediaParser:
    def fetch_matches(self, limit: int = 20):
        response = requests.get(URL, headers=HEADERS)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        matches = []

        for table in soup.select(".wikitable"):
            for row in table.select("tr"):
                cols = row.find_all("td")
                if len(cols) < 3:
                    continue

                time_str = cols[0].get_text(strip=True)
                # Проверяем, что cols[0] — это тег, и ищем красивое время в span
                if isinstance(cols[0], Tag):
                    spans = cols[0].find_all('span')
                    if spans:
                        time_pretty = spans[-1].get_text(strip=True)
                    else:
                        match = re.search(r'(\w+ \d{1,2}, \d{4} - \d{2}:\d{2}CEST)', time_str)
                        if match:
                            time_pretty = match.group(1)
                        else:
                            time_pretty = time_str[-20:] if len(time_str) > 20 else time_str
                else:
                    time_pretty = time_str[-20:] if len(time_str) > 20 else time_str
                stage = cols[1].get_text(strip=True)
                status = cols[-1].get_text(strip=True)

                teams = [c.get_text(strip=True) for c in cols if "vs" not in c.get_text(strip=True).lower()]
                teams = [t for t in teams if t and t not in [stage, time_str, status]]

                if len(teams) >= 2:
                    team1, team2 = teams[0], teams[1]
                else:
                    team1, team2 = "TBD", "TBD"

                if not time_str:
                    continue

                matches.append({
                    "stage": stage,
                    "team1": team1,
                    "team2": team2,
                    "time": time_pretty,
                    "status": status or "TBD"
                })

        return matches[:limit]