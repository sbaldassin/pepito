import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.event_factory import create_parimutuel_event
from tests.factory.wager_factory import create_parimutuel

from tests.utils.utils import get_api_headers, get_api_error_wager_list_empty, get_api_error_player_id_not_passed, \
    get_api_ok_message, get_player_sign_up_resource, \
    get_player_sign_in_resource, get_wagers_parimutuel_resource, get_task_error_invalid_event, \
    get_task_error_invalid_currency, get_task_error_invalid_breed, get_task_error_invalid_wager_value
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class WagerParimutuelTestCase(TestCase):

    def setUp(self):
        super(WagerParimutuelTestCase, self)

    def create_and_validate_player(self, player, channel=1):
        player_sign_up_response = requests.post(get_player_sign_up_resource(channel=channel),
                                                data=json.dumps(player.__dict__),
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
        player_sign_in_response = requests.post(get_player_sign_in_resource(player_id=player.PlayerID, channel=channel),
                                                headers=get_api_headers())
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

    @retry(Exception)
    def verify_wager_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'], error)

    def get_signin(self, player):
        return requests.get("http://{}/sign_in?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_wager_parimutuel(self, player):
        url = "http://{}/wagers/parimutuel?customer_id={}".format(get_config().get("test_framework", "db"),
                                                                  player.PlayerID)
        return get_until_not_empty(url)

    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=100)

    def test_tc_1_wager_parimutuel_example(self):
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
        for wager in q_net_wager_list:
            self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])
            self.assertEqual(signin_id, wager['SignInID'])

    def test_tc_2_wager_parimutuel_without_player_id(self):
        data = {"PlayerID": None, "Wagers": []}

        wager_parimutuel_response = requests.post(get_wagers_parimutuel_resource(),
                                                  data=json.dumps(data),
                                                  headers=get_api_headers())
        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_player_id_not_passed())
        self.assertEqual(body.get('RequestID'), 0)

    def test_tc_3_wager_parimutuel_without_initid(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers()
        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        for wager in q_net_wager_list:
            self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])
            self.assertEqual(0, wager['SignInID'])

    def test_tc_4_wager_parimutuel_without_event(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers(add_event=False)

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertFalse(q_net_wager_list)

        self.verify_wager_error(request_id, get_task_error_invalid_event())

    def test_tc_5_wager_parimutuel_without_breed(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers(add_event=True)

        for w in wagers:
            del w["Breed"]

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertFalse(q_net_wager_list)
        self.verify_wager_error(request_id, get_task_error_invalid_breed())

    def test_tc_6_wager_parimutuel_without_eventdate(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager

        wagers = self.create_wagers()
        for w in wagers:
            w['EventDate'] = None

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        for wager in q_net_wager_list:
            self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])

    def test_tc_7_wager_parimutuel_without_eventid(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers()
        for w in wagers:
            w['EventID'] = None

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        for wager in q_net_wager_list:
            self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])

    def test_tc_8_wager_parimutuel_without_currency(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers(add_event=True)

        for w in wagers:
            del w["Currency"]

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertFalse(q_net_wager_list)
        self.verify_wager_error(request_id, get_task_error_invalid_currency())

    def test_tc_9_wager_parimutuel_without_value(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers(add_event=True)

        for w in wagers:
            del w["Value"]

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertFalse(q_net_wager_list)
        self.verify_wager_error(request_id, get_task_error_invalid_wager_value())

    # def test_tc_10_wager_parimutuel_without_transactiondate(self):
    #     player = create_random_player(player_id_length=40)
    #     logging.info("Creating player: {}".format(player.__dict__))
    #
    #     # Create player
    #     self.create_and_validate_player(player)
    #
    #     # Create Wager
    #     wagers = self.create_wagers()
    #     for w in wagers:
    #         del w['TransactionDate']
    #
    #     data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
    #     q_net_wager_list = self.get_wager_parimutuel(player)
    #     self.assertEqual(len(q_net_wager_list), len(data['Wagers']))
    #
    #     for wager in q_net_wager_list:
    #         self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])
    #         self.assertTrue(wager['DateCreated'])

    def test_tc_11_wager_parimutuel_without_count_0(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))

        # Create player
        self.create_and_validate_player(player)

        # Create Wager
        wagers = self.create_wagers()
        for w in wagers:
            w['Count'] = 0

        data, request_id = self.create_and_validate_wager_parimutuel(player, wagers)
        q_net_wager_list = self.get_wager_parimutuel(player)
        self.assertEqual(len(q_net_wager_list), len(data['Wagers']))

        for wager in q_net_wager_list:
            self.assertEqual(player.PlayerID, wager['ExternalCustomerID'])
            self.assertEqual(1, wager['WagerCount'])

    def test_tc_12_wager_parimutuel_empty_wagers_list(self):
        # New test
        player = create_random_player(player_id_length=40)
        data = {"PlayerID": player.PlayerID, "Wagers": []}

        wager_parimutuel_response = requests.post(get_wagers_parimutuel_resource(),
                                                  data=json.dumps(data),
                                                  headers=get_api_headers())

        self.assertTrue(wager_parimutuel_response.status_code, 200)
        body = wager_parimutuel_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_wager_list_empty())
        self.assertEqual(body.get('RequestID'), 0)