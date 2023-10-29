from src.client.metacritic import MetacriticClient

import unittest
from unittest.mock import patch, Mock
from src.client.metacritic import MetacriticClient, Game

class TestMetacriticClient(unittest.TestCase):
    def setUp(self):
        self.client = MetacriticClient()

    @patch('src.client.metacritic.requests.request')
    def test_search_game(self, mock_request):
        mock_game = {
            "title": "The Legend of Zelda: Breath of the Wild",
            "criticScoreSummary": {"score": 97},
            "releaseDate": "Mar 3, 2017",
            "platforms": [{"name": "Nintendo Switch"}, {"name": "Wii U"}]
        }
        mock_response = Mock()
        mock_response.json.return_value = {
            "components": [{
                "data": {"items": [mock_game]}
            }]
        }
        mock_request.return_value = mock_response

        games = self.client.search_game("zelda")
        expected_game = Game(
            title="The Legend of Zelda: Breath of the Wild",
            score=97,
            release_date="Mar 3, 2017",
            platforms=["Nintendo Switch", "Wii U"]
        )
        self.assertEqual(games, [expected_game])
