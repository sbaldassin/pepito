import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue
from tests.utils.generator import generate_random_int
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_withdrawal_resource, \
    get_deposit_resource

logging.basicConfig(level=logging.INFO)


class DepositTestCase(TestCase):

    def setUp(self):
        super(DepositTestCase, self)

    def test_tc_1_player_revenue(self):
        player, deposit = self._create_player_with_revenue()
        result = self.get_revenue_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertEquals(deposit.amount, result[0]["Amount"])


    @staticmethod
    def get_revenue_from_db(player):
        url = "http://{}/deposits?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url)

    @staticmethod
    def _create_player_with_revenue(revenue=None):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(),
                                 data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        body = response.json()
        logging.info("API response: {}".format(body))

        revenue = create_revenue() if revenue is None else revenue
        logging.info("Creating revenue: {}".format(revenue.__dict__))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(), "Transactions": [revenue.__dict__]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_deposit_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return player, revenue