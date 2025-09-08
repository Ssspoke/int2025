import requests
from bs4 import BeautifulSoup

class LiquipediaParser:
    BASE_URL = "https://liquipedia.net/dota2/The_International/2025"

    def fetch_matches(self):
        response = requests.get(self.BASE_URL, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        # Пример парсинга: ищем таблицы с матчами (может потребоваться доработка под реальную верстку)
        for table in soup.find_all('table', class_='wikitable'):  # Класс может отличаться!
            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    match = {
                        'team1': cols[1].get_text(strip=True),
                        'team2': cols[3].get_text(strip=True),
                        'time': cols[0].get_text(strip=True),
                        'status': cols[4].get_text(strip=True)
                    }
                    matches.append(match)
        return matches
