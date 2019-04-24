import datetime
import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.withdrawal_factory import create_withdrawal
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_withdrawal_resource

logging.basicConfig(level=logging.INFO)


class WithdrawalTestCase(TestCase):

    def setUp(self):
        super(WithdrawalTestCase, self)

    def test_tc_1_player_withdrawal(self):
        player, withdrawal = self._create_player_with_withdrawal()
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(withdrawal.amount, result[0]["Amount"])

    def test_tc_2_player_withdrawal_with_eur_currency(self):
        withdrawal = create_withdrawal()
        withdrawal.currency = "EUR"
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(withdrawal.amount, result[0]["Amount"])

    def test_tc_3_player_withdrawal_with_invalid_currency(self):
        withdrawal = create_withdrawal()
        withdrawal.currency = 123
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_4_player_withdrawal_with_zero_amount(self):
        withdrawal = create_withdrawal()
        withdrawal.amount = 0
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_5_player_withdrawal_with_negative_amount(self):
        withdrawal = create_withdrawal()
        withdrawal.amount = -1
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_6_player_withdrawal_with_string_amount(self):
        withdrawal = create_withdrawal()
        withdrawal.amount = "sdk"
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    def test_tc_7_player_withdrawal_with_future_date(self):
        withdrawal = create_withdrawal()
        withdrawal.transaction_date = datetime.datetime(2030, 4, 24, 18, 26, 1, 37000).strftime('%Y-%m-%d')
        player, withdrawal = self._create_player_with_withdrawal(withdrawal)
        result = self.get_withdrawal_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertTrue(result == [])

    @staticmethod
    def get_withdrawal_from_db(player):
        url = "http://{}/withdrawals?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url)

    @staticmethod
    def _create_player_with_withdrawal(withdrawal=None):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(),
                                 data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        body = response.json()
        logging.info("API response: {}".format(body))

        withdrawal = create_withdrawal() if withdrawal is None else withdrawal
        logging.info("Creating withdrawal: {}".format(withdrawal.__dict__))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(), "Withdrawals": [withdrawal.__dict__]}
        response = requests.post(get_withdrawal_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return player, withdrawal
