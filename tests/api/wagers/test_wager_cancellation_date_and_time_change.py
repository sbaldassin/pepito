import json
import logging
from unittest import TestCase, skip
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_parimutuel_wager
from tests.factory.event_factory import create_parimutuel_event
from tests.utils.utils import get_api_headers, get_player_sign_up_resource, get_api_ok_message, \
    get_player_sign_in_resource, get_wagers_parimutuel_resource

logging.basicConfig(level=logging.INFO)


class PlayerSignInTestCase(TestCase):

    def setUp(self):
        super(PlayerSignInTestCase, self)
    
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
        self.assertEqual(body.get('Result').get('Success'), True)
        self.assertEqual(body.get('Result').get('Message'), get_api_ok_message())
        signin_id = body.get('ID')
        self.assertTrue(signin_id)
    
        q_net_signin = self.get_signin(player)[0]
        self.assertEqual(signin_id, q_net_signin['SignInID'])
        return signin_id

    def create_and_validate_wager_parimutuel(self, player, signin_id, channel=1, total_wagers=1):
        wagers = []
        for i in range(total_wagers):
            wager = create_parimutuel_wager().__dict__
            event = create_parimutuel_event().__dict__
            wager.update(event)
            wagers.append(wager)

        data = {"PlayerID": player.PlayerID, "InitID": signin_id,
                "Wagers": wagers}
        
        wager_parimutuel_response = requests.post(get_wagers_parimutuel_resource(channel=channel),
                                                data=json.dumps(data),
                                                headers=get_api_headers())
        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        logging.info("Wager Parimutuel API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)
        
        q_net_wager_list = self.get_wager_parimutuel(player)
        # TODO: add timeout or related
        #self.assertEqual(len(q_net_wager_list), len(wagers))
        
        return data
    
    def cancel_wagers_parimutuel(self, data):
        wager_parimutuel_response = requests.delete(get_wagers_parimutuel_resource(channel=''),
                                                data=json.dumps(data),
                                                headers=get_api_headers())
        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        logging.info("Cancel Wager Parimutuel API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        
    def get_signin(self, player):
        return requests.get("http://{}/sign_in?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()
    
    def get_wager_parimutuel(self, player):
        return requests.get("http://{}/wagers/parimutuel?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def test_tc_1_wager_creation_cancellation(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)
        signin_id = self.create_and_validate_signin(player, channel)
        
        # Create Wager
        data = self.create_and_validate_wager_parimutuel(player, signin_id, channel)

        # Cancel Wager
        self.cancel_wagers_parimutuel(data)
