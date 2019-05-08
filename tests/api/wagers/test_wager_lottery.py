import json
import logging
from unittest import TestCase
import requests
from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_wager_lottery
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_wager_lottery_resource

logging.basicConfig(level=logging.INFO)


class WagerLotteryTestCase(TestCase):

    def setUp(self):
        super(WagerLotteryTestCase, self)

    def test_tc_1_player_wager(self):
        player, wager = self._create_player_with_wager()
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroCentsValue"] != 0)


    @staticmethod
    def get_wager_from_db(player):
        url = "http://{}/wagers?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url)

    @staticmethod
    def _create_player():
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(),
                                 data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        body = response.json()
        logging.info("API response: {}".format(body))
        return player

    @staticmethod
    def _create_wagers(player, wagers=[]):
        _wagers = [create_wager_lottery()] if wagers == [] else wagers
        logging.info("Creating wagers: {}".format([r.__dict__ for r in _wagers]))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(),
                "Wagers": [r.__dict__ for r in _wagers]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_wager_lottery_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return wagers

    def _create_player_with_wager(self, wagers=[]):
        player = self._create_player()
        wagers = self._create_wagers(player, wagers)
        return player, wagers
