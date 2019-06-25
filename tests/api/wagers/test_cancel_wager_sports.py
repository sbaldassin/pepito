import json
import logging
import requests
from unittest import TestCase
from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_sport
from tests.utils.utils import get_api_headers, get_api_error_player_id_not_passed, get_api_ok_message, get_player_sign_up_resource, \
    get_player_sign_in_resource, get_wager_sport_resource, get_task_error_invalid_breed_cancellation, \
    get_task_error_invalid_sport_identifier, get_task_error_invalid_currency, get_task_error_invalid_wager_value, get_task_error_invalid_transaction_date
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class CancelWagerSportsTestCase(TestCase):

    def setUp(self):
        super(CancelWagerSportsTestCase, self)
    
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
            wager = create_sport().__dict__
            # if add_event:
            #     event = create_parimutuel_event().__dict__
            #     wager.update(event)
            wagers.append(wager)
        return wagers

    def create_and_validate_wager_sports(self, player, wagers, signin_id=None, channel=1):
        data = {"PlayerID": player.PlayerID, "InitID": signin_id, "Wagers": wagers}
        
        wager_sports_response = requests.post(get_wager_sport_resource(channel=channel),
                                                data=json.dumps(data),
                                                headers=get_api_headers())
        self.assertTrue(wager_sports_response.status_code, 200)
        body = wager_sports_response.json()
        logging.info("Wager SPoprts API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)
        return data, request_id
    
    def cancel_wagers_sports(self, data):
        wager_parimutuel_response = requests.delete(get_wager_sport_resource(channel=''),
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
    
    def get_wager_sports(self, player):
        url = "http://{}/wagers/parimutuel?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url, timeout=70)
    
    def get_wager_sports_wager_count(self, player, wagercount):
        url = "http://{}/wagers/parimutuel?customer_id={}&wagercount={}".format(get_config().get("test_framework", "db"), player.PlayerID, wagercount)
        return get_until_not_empty(url, timeout=70)
    
    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=40)

    @retry(Exception, tries=5)
    def verify_canceled_wager(self, data, player):
        for wager in data['Wagers']:
            wc = wager['Count'] * -1
            q_net_wager_list = self.get_wager_sports_wager_count(player, wc)
            self.assertTrue(q_net_wager_list)

    @retry(Exception, tries=6)
    def verify_canceled_wager_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'], error)

    def test_tc_1_cancel_wager_sports_example(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)
        signin_id = self.create_and_validate_signin(player, channel)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers, signin_id, channel)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
        
        # Cancel Wager
        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    def test_tc_2_cancel_wager_sports_without_player_id(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        channel = 1
        self.create_and_validate_player(player, channel)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)
        data["PlayerID"] = None

        wager_parimutuel_response = requests.delete(get_wager_sport_resource(channel=''),
                                                    data=json.dumps(data),
                                                    headers=get_api_headers())

        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_player_id_not_passed())
        self.assertEqual(body.get('RequestID'), 0)

    def test_tc_3_cancel_wager_sports_without_initid(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager
        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    # BUG: expected error is 'Invalid Sport identifier on record number 1. No data saved.'
    #      current error: "Object reference not set to an instance of an object."
    def atc_4_cancel_wager_parimutuel_without_sport(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)
        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['Sport'] = None

        request_id = self.cancel_wagers_sports(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_sport_identifier())

    # BUG: expected error is 'Invalid League/tournament identifier on record number 1. No data saved.'
    #      current error: "Object reference not set to an instance of an object."
    def attest_tc_5_cancel_wager_sports_without_league(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['League'] = None

        request_id = self.cancel_wagers_sports(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_breed_cancellation())

    # Bug idem to tc 4 & 5
    def attest_tc_6_cancel_wager_sports_without_event(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['Event'] = None

        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    #Error: Wager not found. Couldn't proceed with wager cancellation.

    def ttest_tc_7_cancel_wager_sports_without_live(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without live
        for w in data['Wagers']:
            w['Live'] = None

        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    def atest_tc_8_cancel_wager_parimutuel_without_event_date(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event date
        for w in data['Wagers']:
            w['EventDate'] = None

        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    #BUG "Object reference not set to an instance of an object."
    def ttest_tc_9_cancel_wager_parimutuel_without_event_id(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event id
        for w in data['Wagers']:
            w['EventID'] = None

        self.cancel_wagers_sports(data)
        self.verify_canceled_wager(data, player)

    def test_tc_10_cancel_wager_sports_without_currency(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['Currency'] = None

        request_id = self.cancel_wagers_sports(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_currency())

    def test_tc_11_cancel_wager_sports_without_value(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['Value'] = None

        request_id = self.cancel_wagers_sports(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_wager_value())

    def test_tc_12_cancel_wager_sports_without_transaction_date(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        wagers = self.create_wagers()
        # Create Wager
        data, request_id = self.create_and_validate_wager_sports(player, wagers)

        q_net_wager_list = self.get_wager_sports(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        # Cancel Wager without event
        for w in data['Wagers']:
            w['TransactionDate'] = None

        # SqlDateTime overflow. Must be between 1/1/1753 12:00:00 AM and 12/31/9999 11:59:59 PM
        request_id = self.cancel_wagers_sports(data)
        self.verify_canceled_wager_error(request_id, get_task_error_invalid_transaction_date())
