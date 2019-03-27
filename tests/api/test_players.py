import json
import logging
from unittest import TestCase
import requests

from tests.db.mssql_driver import MsSqlDriver
from tests.factory.player_factory import create_random_player


API_URL = "http://qa-apx-aretonet.azurewebsites.net/player"
logging.basicConfig(level=logging.INFO)


class PlayersTestCase(TestCase):

    def test_sign_up(self):
        player = create_random_player()
        logging.info("Creating player: {}".format(player.__dict__))

        response = requests.post(API_URL, data=json.dumps(player.__dict__))
        self.assertTrue(response.status_code, 200)
        self.assertIsNotNone(MsSqlDriver().get_player(player))