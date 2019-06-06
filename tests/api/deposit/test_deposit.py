import datetime
import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_deposit_resource

logging.basicConfig(level=logging.INFO)


class DepositTestCase(TestCase):

    def setUp(self):
        super(DepositTestCase, self)

    def test_tc_1_player_revenue(self):
        player, revenues = self._create_player_with_revenue()
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroAmount"] != 0)

    def test_tc_2_player_revenue_with_eur_currency(self):
        revenue = create_revenue()
        revenue.Currency = "EUR"
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(int(revenue.Amount) * 100, result[0]["EuroAmount"])

    def test_tc_3_player_revenue_with_invalid_currency(self):
        revenue = create_revenue()
        revenue.Currency = 123
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_4_player_revenue_with_zero_amount(self):
        revenue = create_revenue()
        revenue.Amount = 0
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_5_player_revenue_with_negative_amount(self):
        revenue = create_revenue()
        revenue.Amount = -1
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_6_player_revenue_with_string_amount(self):
        revenue = create_revenue()
        revenue.Amount = "sdk"
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_7_player_revenue_with_future_date(self):
        revenue = create_revenue()
        revenue.TransactionDate = datetime.datetime(2030, 4, 24, 18, 26, 1, 37000).strftime('%Y-%m-%d')
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_8_player_revenue_with_invalid_date(self):
        revenue = create_revenue()
        revenue.TransactionDate = "hah"
        player, revenue = self._create_player_with_revenue([revenue])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_9_player_revenue_with_multiple_transactions(self):
        revenue_1 = create_revenue()
        revenue_2 = create_revenue()
        player, revenues = self._create_player_with_revenue(revenues=[revenue_1, revenue_2])
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(len(result), 2)

    @staticmethod
    def get_revenue_from_db(player):
        url = "http://{}/deposits?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
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
    def _create_revenues(player, revenues=[]):
        revenues = [create_revenue()] if revenues is [] else revenues
        logging.info("Creating revenue: {}".format([r.__dict__ for r in revenues]))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(),
                "Transactions": [r.__dict__ for r in revenues]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_deposit_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return revenues

    def _create_player_with_revenue(self, revenues=[]):
        player = self._create_player()
        revenues = self._create_revenues(player, revenues)
        return player, revenues
