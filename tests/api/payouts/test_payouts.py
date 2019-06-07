import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.payout_factory import create_payout
from tests.factory.player_factory import create_random_player

from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_payout_resource

logging.basicConfig(level=logging.INFO)


class PayoutTestCase(TestCase):

    def setUp(self):
        super(PayoutTestCase, self)

    def test_tc_1_player_payout_casino(self):
        player, payout = self._create_player_with_payout(payout_type="casino")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_2_player_payout_sport(self):
        player, payout = self._create_player_with_payout(payout_type="sport")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_3_player_payout_sport(self):
        player, payout = self._create_player_with_payout(payout_type="bet")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_4_player_payout_esport(self):
        player, payout = self._create_player_with_payout(payout_type="esport")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_5_player_payout_esport(self):
        player, payout = self._create_player_with_payout(payout_type="lottery")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_6_player_payout_esport(self):
        player, payout = self._create_player_with_payout(payout_type="parimutuel")
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    @staticmethod
    def get_payout_from_db(player):
        url = "http://{}/payouts?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url, timeout=240)

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
    def _create_payouts(player, payout_type, payouts=[]):
        _payouts = [create_payout(payout_type=payout_type)] if payouts == [] else payouts
        logging.info("Creating payouts: {}".format([r.__dict__ for r in _payouts]))

        data = {"PlayerID": player.PlayerID, "InitID": int(generate_random_int()),
                "Payouts": [r.__dict__ for r in _payouts]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_payout_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return payouts

    def _create_player_with_payout(self, payout_type, payouts=[]):
        player = self._create_player()
        payouts = self._create_payouts(player, payout_type, payouts)
        return player, payouts
