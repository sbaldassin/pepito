import json
import logging
from unittest import TestCase
import requests

from tests.db.mssql_driver import MsSqlDriver
from tests.factory.player_factory import create_random_player


API_URL = 'http://qa-apx-aretonet.azurewebsites.net/player/signup/1'
logging.basicConfig(level=logging.INFO)


class PlayersTestCase(TestCase):

    def test_sign_up(self):
        player = create_random_player()
        logging.info("Creating player: {}".format(player.__dict__))
        headers = {
            'Authorization': 'Bearer SSP-7A39E3C6-D7AB-420C-A4B1-4E099DF3B377',
            'Content-Type': 'application/json'
        }
        response = requests.post(API_URL, data=json.dumps(player.__dict__), headers=headers)
        body = response.json()
        self.assertTrue(response.status_code, 200)
        self.assertTrue(body.get('Success'), True)
        self.assertIsNotNone(MsSqlDriver().get_player(player))
