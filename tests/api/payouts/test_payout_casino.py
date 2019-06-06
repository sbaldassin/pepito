import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.payout_factory import create_casino
from tests.factory.player_factory import create_random_player

from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_payout_casino_resource

logging.basicConfig(level=logging.INFO)


class PayoutCasinoTestCase(TestCase):

    def setUp(self):
        super(PayoutCasinoTestCase, self)

    def test_tc_1_player_payout_casino(self):
        player, payout = self._create_player_with_payout()
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
    def _create_payouts(player, payouts=[]):
        _payouts = [create_casino()] if payouts == [] else payouts
        logging.info("Creating payouts: {}".format([r.__dict__ for r in _payouts]))

        data = {"PlayerID": player.PlayerID, "InitID": int(generate_random_int()),
                "Payouts": [r.__dict__ for r in _payouts]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_payout_casino_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return payouts

    def _create_player_with_payout(self, payouts=[]):
        player = self._create_player()
        payouts = self._create_payouts(player, payouts)
        return player, payouts
