import requests
from dataclasses import dataclass
from typing import List

@dataclass
class Game:
    title: str
    score: int
    release_date: str
    platforms: List[str]

class MetacriticClient:
    def __init__(self):
        self.url = "https://fandom-prod.apigee.net/v1/xapi/composer/metacritic/pages/search/"
        self.payload = {}
        self.headers = {}

    def search_game(self, game_query):
        url = self.url + game_query + "/web"
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        response_json = response.json()
        items = response_json["components"][0]["data"]["items"]
        games = []
        for item in items:
            if item["criticScoreSummary"]["score"] is not None:
                game = Game(
                    title=item["title"],
                    score=item["criticScoreSummary"]["score"],
                    release_date=item["releaseDate"],
                    platforms=[platform["name"] for platform in item["platforms"]]
                )
                games.append(game)
        return games