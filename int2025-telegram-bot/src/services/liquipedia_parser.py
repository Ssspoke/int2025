import requests
from bs4 import BeautifulSoup
from datetime import datetime
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

                stage = cols[0].get_text(strip=True)
                time = cols[1].get_text(strip=True)
                status = cols[-1].get_text(strip=True)

                teams = [c.get_text(strip=True) for c in cols if "vs" not in c.get_text(strip=True).lower()]
                teams = [t for t in teams if t and t not in [stage, time, status]]

                if len(teams) >= 2:
                    team1, team2 = teams[0], teams[1]
                else:
                    team1, team2 = "TBD", "TBD"

                if not time:
                    continue

                # переводим время из CEST в MSK
                try:
                    match_time = datetime.strptime(time, "%Y-%m-%d %H:%M").replace(
                        tzinfo=ZoneInfo("Europe/Berlin")
                    )
                    moscow_time = match_time.astimezone(ZoneInfo("Europe/Moscow"))
                    time = moscow_time.strftime("%Y-%m-%d %H:%M MSK")
                except Exception:
                    pass

                matches.append({
                    "stage": stage,
                    "team1": team1,
                    "team2": team2,
                    "time": time,
                    "status": status or "TBD"
                })

        return matches[:limit]
