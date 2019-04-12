import json
import logging
from unittest import TestCase
import requests

from tests.db.mssql_driver import MsSqlDriver
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource

logging.basicConfig(level=logging.WARNING)


class PlayersTestCase(TestCase):

    def test_sign_up(self):
        player = create_random_player()
        logging.info("Creating player: {}".format(player.__dict__))
        headers = {
            'Authorization': 'Bearer SSP-7A39E3C6-D7AB-420C-A4B1-4E099DF3B377',
            'Content-Type': 'application/json'
        }
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        self.assertTrue(body.get('Success'), True)
        self.assertIsNotNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNotNone(MsSqlDriver().get_player_from_fact_signup(player))
