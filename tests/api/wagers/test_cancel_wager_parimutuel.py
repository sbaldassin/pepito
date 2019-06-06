import json
import logging
import requests
from unittest import TestCase

from tests.config.config import get_config
from tests.factory.event_factory import create_parimutuel_event
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_parimutuel
from tests.utils.utils import get_api_headers, get_api_error_player_id_not_passed, get_api_ok_message, get_player_sign_up_resource, \
    get_player_sign_in_resource, get_wagers_parimutuel_resource, get_task_error_invalid_breed_cancellation, \
    get_task_error_invalid_event, get_task_error_invalid_currency_cancellation, get_task_error_invalid_value_cancellation, get_task_error_sql_overflow
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class CancelWagerParimutuelTestCase(TestCase):

    def setUp(self):
        super(CancelWagerParimutuelTestCase, self)
    
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
    
    def create_wagers(self, total_wagers=1, add_event=True):
        wagers = []
        for i in range(total_wagers):
            wager = create_parimutuel().__dict__
            if add_event:
                event = create_parimutuel_event().__dict__
                wager.update(event)
            wagers.append(wager)
        return wagers

    def create_and_validate_wager_parimutuel(self, player, wagers, signin_id=None, channel=1):
        data = {"PlayerID": player.PlayerID, "InitID": signin_id, "Wagers": wagers}
        
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
        return data, request_id
    
    def cancel_wagers_parimutuel(self, data):
        wager_parimutuel_response = requests.delete(get_wagers_parimutuel_resource(channel=''),
                                                data=json.dumps(data),
                                                headers=get_api_headers())
        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        logging.info("Cancel Wager Parimutuel API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)
        return request_id
        
    def get_signin(self, player):
        url = "http://{}/sign_in?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url)

    def get_customer(self, player):
        url = "http://{}/customer?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url)
    
    def get_wager_parimutuel(self, player):
        url = "http://{}/wagers/parimutuel?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url, timeout=50)
    
    def get_wager_parimutuel_wager_count(self, player, wagercount):
        url = "http://{}/wagers/parimutuel?customer_id={}&wagercount={}".format(get_config().get("test_framework", "db"), player.PlayerID, wagercount)
        return get_until_not_empty(url, timeout=50)
    
    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=40)

    @retry(Exception, tries=5)
    def verify_canceled_wager(self, data, player):
        for wager in data['Wagers']:
            wc = wager['Count'] * -1
            q_net_wager_list = self.get_wager_parimutuel_wager_count(player, wc)
            self.assertTrue(q_net_wager_list)

    @retry(Exception, tries=6)
    def verify_canceled_wager_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'], error)
        
    def test_tc_1_cancel_wager_parimutuel_example(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)
        signin_id = self.create_and_validate_signin(player, channel)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers, signin_id, channel)

        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
        
        # Cancel Wager
        self.verify_canceled_wager(data, player)

    def test_tc_2_cancel_wager_parimutuel_without_player_id(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        data["PlayerID"] = None

        wager_parimutuel_response = requests.delete(get_wagers_parimutuel_resource(channel=''),
                                                    data=json.dumps(data),
                                                    headers=get_api_headers())
        
        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_player_id_not_passed())
        self.assertEqual(body.get('RequestID'), 0)

    def test_tc_3_cancel_wager_parimutuel_without_initid(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager
        self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager(data, player)

    def tc_4_cancel_wager_parimutuel_without_event(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['Event'] = None
            
        request_id = self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_event())

    def test_tc_5_cancel_wager_parimutuel_without_breed(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['Breed'] = None
            
        request_id = self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_breed_cancellation())

    def test_tc_6_cancel_wager_parimutuel_without_event_date(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['EventDate'] = None
        
        self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager(data, player)

    def test_tc_7_cancel_wager_parimutuel_without_event_id(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['EventID'] = None
            
        self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager(data, player)

    def test_tc_8_cancel_wager_parimutuel_without_currency(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['Currency'] = None
            
        request_id = self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_currency_cancellation())

    def test_tc_9_cancel_wager_parimutuel_without_value(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['Value'] = None
        
        request_id = self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_value_cancellation())

    def test_tc_10_cancel_wager_parimutuel_without_transaction_date(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        self.create_and_validate_player(player)
    
        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    
        # Cancel Wager without event
        for w in data['Wagers']:
            w['TransactionDate'] = None

        # SqlDateTime overflow. Must be between 1/1/1753 12:00:00 AM and 12/31/9999 11:59:59 PM
        request_id = self.cancel_wagers_parimutuel(data)
        self.verify_canceled_wager_error(request_id, get_task_error_sql_overflow())