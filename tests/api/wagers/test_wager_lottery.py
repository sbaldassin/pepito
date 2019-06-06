import datetime
import json
import logging
from unittest import TestCase
import requests
from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_lottery
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_wager_lottery_resource

logging.basicConfig(level=logging.INFO)


class WagerLotteryTestCase(TestCase):

    def setUp(self):
        super(WagerLotteryTestCase, self)

    def test_tc_1_player_wager_lottery(self):
        player, wager = self._create_player_with_wager()
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroCentsValue"] != 0)

    def test_tc_2_wager_lottery_invalid_currency(self):
        wager = create_lottery()
        wager.Currency = "Invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_3_wager_lottery_usd_currency(self):
        wager = create_lottery()
        wager.Currency = "USD"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_4_wager_lottery_invalid_value(self):
        wager = create_lottery()
        wager.Value = "Invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_5_wager_lottery_negative_value(self):
        wager = create_lottery()
        wager.Value = -1
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_6_wager_lottery_zero_value(self):
        wager = create_lottery()
        wager.Value = 0
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_7_wager_lottery_huge_value(self):
        wager = create_lottery()
        wager.Value = 100000000000
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_8_wager_lottery_zero_count(self):
        wager = create_lottery()
        wager.Count = 0
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_9_wager_lottery_negative_count(self):
        wager = create_lottery()
        wager.Count = -1
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_10_wager_lottery_invalid_count(self):
        wager = create_lottery()
        wager.Count = "invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_11_wager_lottery_huge_count(self):
        wager = create_lottery()
        wager.Count = 100000000000
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_12_wager_lottery_invalid_category(self):
        wager = create_lottery()
        wager.Category = "invalid"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_13_wager_lottery_invalid_transaction_date(self):
        wager = create_lottery()
        wager.TransactionDate = "invalid_date"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_14_wager_lottery_future_transaction_date(self):
        wager = create_lottery()
        wager.TransactionDate = datetime.datetime(2030, 4, 24, 18, 26, 1, 37000).strftime('%Y-%m-%d')
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_15_wager_lottery_invalid_draw_date(self):
        wager = create_lottery()
        wager.DrawDate = "invalid_date"
        player, revenue = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_16_wager_lottery_future_draw_date(self):
        wager = create_lottery()
        wager.DrawDate = datetime.datetime(2030, 4, 24, 18, 26, 1, 37000).strftime('%Y-%m-%d')
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
        _wagers = [create_lottery()] if wagers == [] else wagers
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
