import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource, get_player_update_resource, get_api_ok_message

logging.basicConfig(level=logging.INFO)


class PlayerUpdateTestCase(TestCase):

    def setUp(self):
        super(PlayerUpdateTestCase, self)

    def test_tc_1_player_id_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        player_sign_up_response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        
        self.assertTrue(player_sign_up_response.status_code, 200)
        body = player_sign_up_response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())

        q_net_customer = self.get_customer(player)
        q_net_dw_fact_signup = self.get_signup(player)
        
        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEqual(player.PlayerID, q_net_customer['ExternalCustomerID'])
        self.assertEqual(player.Email, q_net_customer['Email'])

        # Update player
        player.PlayerID = player.PlayerID + player.PlayerID[-1]
        player_update_response = requests.post(get_player_update_resource(), data=json.dumps(player.__dict__),
                                               headers=get_api_headers())

        self.assertTrue(player_update_response.status_code, 200)
        body = player_sign_up_response.json()
        self.assertEqual(body.get('Success'), True)
    
        updated_q_net_customer = self.get_customer(player)
        self.assertTrue(updated_q_net_customer)
        self.assertEqual(player.PlayerID, updated_q_net_customer['ExternalCustomerID'])
        self.assertEqual(player.Email, updated_q_net_customer['Email'])
        self.assertEqual(player.Name, updated_q_net_customer['Name'])
        self.assertEqual(player.Surname, updated_q_net_customer['Surname'])
        
    def get_signup(self, player):
        return requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]
