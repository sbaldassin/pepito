import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource, get_api_ok_message, get_player_flush_resource

logging.basicConfig(level=logging.INFO)


class PlayerSignInTestCase(TestCase):

    def setUp(self):
        super(PlayerSignInTestCase, self)
    
    def create_and_validate_player(self, player):
        player_sign_up_response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                                headers=get_api_headers())
        self.assertTrue(player_sign_up_response.status_code, 200)
        body = player_sign_up_response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        
        q_net_customer_list = self.get_customer(player)
        self.assertEqual(len(q_net_customer_list), 1)
        q_net_customer = q_net_customer_list[0]
        self.assertTrue(q_net_customer)
        self.assertEqual(player.PlayerID, q_net_customer['ExternalCustomerID'])
        self.assertEqual(player.Email, q_net_customer['Email'])

    def flush_player_and_validate(self, player):
        player_sign_in_response = requests.delete(get_player_flush_resource(player_id=player.PlayerID), headers=get_api_headers())
        self.assertTrue(player_sign_in_response.status_code, 200)
        body = player_sign_in_response.json()
        logging.info("API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())

        q_net_customer_list = self.get_customer(player)
        q_net_customer = q_net_customer_list[0]
        flushed = "<flushed>"
        self.assertEqual(flushed, q_net_customer['City'])
        
    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()
    
    def test_tc_1_flush_player(self):
        player = create_random_player(player_id_length=20)
        logging.info("Creating player: {}".format(player.__dict__))
        # Create player
        self.create_and_validate_player(player)

        # Flush
        self.flush_player_and_validate(player)

    def test_tc_2_flush_without_player_id(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        
        self.create_and_validate_player(player)
    
        # Signin_channel_1
        player.PlayerID = ''
        player_sign_in_response = requests.delete(get_player_flush_resource(player_id=player.PlayerID), headers=get_api_headers())
        self.assertTrue(player_sign_in_response.status_code, 404)