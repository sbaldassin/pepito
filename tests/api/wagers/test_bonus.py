import datetime
import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.bonus_factory import create_bonus
from tests.factory.player_factory import create_random_player
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_bonus_resource

logging.basicConfig(level=logging.INFO)


class BonusTestCase(TestCase):

    def setUp(self):
        super(BonusTestCase, self)

    def test_tc_1_player_bonus(self):
        player, bonuses = self._create_player_with_bonus()
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroAmount"] != 0)

    def test_tc_2_player_bonus_with_eur_currency(self):
        bonus = create_bonus()
        bonus.Currency = "EUR"
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(int(bonus.Amount) * 100, result[0]["EuroAmount"])

    def test_tc_3_player_bonus_with_invalid_currency(self):
        bonus = create_bonus()
        bonus.Currency = 123
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_4_player_bonus_with_zero_amount(self):
        bonus = create_bonus()
        bonus.Amount = 0
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_5_player_bonus_with_negative_amount(self):
        bonus = create_bonus()
        bonus.Amount = -1
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_6_player_bonus_with_string_amount(self):
        bonus = create_bonus()
        bonus.Amount = "sdk"
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_7_player_bonus_with_future_date(self):
        bonus = create_bonus()
        bonus.TransactionDate = datetime.datetime(2030, 4, 24, 18, 26, 1, 37000).strftime('%Y-%m-%d')
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_8_player_bonus_with_invalid_date(self):
        bonus = create_bonus()
        bonus.TransactionDate = "hah"
        player, bonus = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_9_player_bonus_with_multiple_transactions(self):
        bonus_1 = create_bonus()
        bonus_2 = create_bonus()
        player, bonuses = self._create_player_with_bonus(bonuses=[bonus_1, bonus_2])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(len(result), 2)

    def test_tc_10_player_bonus_with_invalid_productID(self):
        bonus = create_bonus()
        bonus.ProductID = "7"
        player, bonuses = self._create_player_with_bonus()
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))
        self.assertFalse(result == [])

    def test_tc_11_bonus_invalid_value(self):
        bonus = create_bonus()
        bonus.Value = "Invalid"
        player, revenue = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_12_bonus_negative_value(self):
        bonus = create_bonus()
        bonus.Value = -1
        player, revenue = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_13_bonus_zero_value(self):
        bonus = create_bonus()
        bonus.Value = 0
        player, revenue = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_14_bonus_huge_value(self):
        bonus = create_bonus()
        bonus.Value = 100000000000
        player, revenue = self._create_player_with_bonus([bonus])
        result = self.get_bonus_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    @staticmethod
    def get_bonus_from_db(player):
        url = "http://{}/bonuses?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        logging.info("Get Bonus from DB: {}".format(player.__dict__))
        return get_until_not_empty(url,timeout=18)

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
    def _create_bonuses(player, bonuses=[]):
        _bonuses = [create_bonus()] if bonuses == [] else bonuses
        logging.info("Creating bonus: {}".format([r.__dict__ for r in _bonuses]))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(),
                "Bonuses": [r.__dict__ for r in _bonuses]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_bonus_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return bonuses

    def _create_player_with_bonus(self, bonuses=[]):
        player = self._create_player()
        bonuses = self._create_bonuses(player, bonuses)
        return player, bonuses
