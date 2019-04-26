import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource, get_player_update_resource,\
    get_api_ok_message, get_player_sign_in_resource

logging.basicConfig(level=logging.INFO)


class PlayerUpdateTestCase(TestCase):

    def setUp(self):
        super(PlayerUpdateTestCase, self)
    
    def create_and_validate_player(self, player, channel=1):
        player_sign_up_response = requests.post(get_player_sign_up_resource(channel=channel), data=json.dumps(player.__dict__),
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

    def create_and_validate_signin(self, player, channel=1):
        player_sign_in_response = requests.post(get_player_sign_in_resource(player_id=player.PlayerID, channel=channel), headers=get_api_headers())
        self.assertTrue(player_sign_in_response.status_code, 200)
        body = player_sign_in_response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        signin_id = body.get('ID')
        self.assertTrue(signin_id)
    
        q_net_signin = self.get_signin(player)
        self.assertEqual(signin_id, q_net_signin['SignInID'])

    def get_signin(self, player):
        return requests.get("http://{}/sign_in?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()
    
    def test_tc_1_signin_channel_1(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)

        # Siging_channel_1
        self.create_and_validate_signin(player, channel)

    def test_tc_2_signin_channel_2(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        channel = 2
        self.create_and_validate_player(player, channel)
    
        # Siging_channel_1
        self.create_and_validate_signin(player, channel)

    def test_tc_3_signin_without_player_id(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        channel = 2
        self.create_and_validate_player(player, channel)
    
        # Signin_channel_1
        player.PlayerID = ''
        player_sign_in_response = requests.post(get_player_sign_in_resource(player_id=player.PlayerID, channel=channel),
                                                headers=get_api_headers())
        self.assertTrue(player_sign_in_response.status_code, 404)

    def test_tc_4_signin_without_player_id(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        channel = 2
        self.create_and_validate_player(player, channel)
    
        # Signin_channel_1
        channel = ''
        player_sign_in_response = requests.post(get_player_sign_in_resource(player_id=player.PlayerID, channel=channel),
                                                headers=get_api_headers())
        self.assertTrue(player_sign_in_response.status_code, 404)

