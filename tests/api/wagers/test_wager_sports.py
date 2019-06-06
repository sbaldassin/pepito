import json
import logging
from unittest import TestCase
import requests
from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_sport
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_wager_sport_resource

logging.basicConfig(level=logging.INFO)


class WagerSportsTestCase(TestCase):

    def setUp(self):
        super(WagerSportsTestCase, self)

    def test_tc_1_player_wager_sport(self):
        player, wager = self._create_player_with_wager()
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroCentsValue"] != 0)

    def test_tc_2_wager_sport_invalid_currency(self):
        wager = create_sport()
        wager.Currency = "Invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_3_wager_sport_usd_currency(self):
        wager = create_sport()
        wager.Currency = "USD"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_4_wager_sport_invalid_value(self):
        wager = create_sport()
        wager.Value = "Invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_5_wager_sport_negative_value(self):
        wager = create_sport()
        wager.Value = -1
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_6_wager_sport_zero_value(self):
        wager = create_sport()
        wager.Value = 0
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_7_wager_sport_huge_value(self):
        wager = create_sport()
        wager.Value = 100000000000
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_8_wager_sport_zero_count(self):
        wager = create_sport()
        wager.Count = 0
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_9_wager_sport_negative_count(self):
        wager = create_sport()
        wager.Count = -1
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_10_wager_sport_invalid_count(self):
        wager = create_sport()
        wager.Count = "invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_11_wager_sport_huge_count(self):
        wager = create_sport()
        wager.Count = 100000000000
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

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
        _wagers = [create_sport()] if wagers == [] else wagers
        logging.info("Creating wagers: {}".format([r.__dict__ for r in _wagers]))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(),
                "Wagers": [r.__dict__ for r in _wagers]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_wager_sport_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return wagers

    def _create_player_with_wager(self, wagers=[]):
        player = self._create_player()
        wagers = self._create_wagers(player, wagers)
        return player, wagers
