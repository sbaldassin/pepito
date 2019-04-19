import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.db.repositories.q_net_customer_repository import QNetCustomerRepository
from tests.db.repositories.q_net_dw_fact_signup_repository import QNetDwFactSignupRepository
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource

logging.basicConfig(level=logging.INFO)


class PlayerRegistrationTestCase(TestCase):

    def setUp(self):
        super(PlayerRegistrationTestCase, self)

    def test_tc_1_player_registration_id_40_chars(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEqual(player.PlayerID, q_net_customer['ExternalCustomerID'])
        self.assertEqual(player.Email, q_net_customer['Email'])
        self.assertEqual(player.Name, q_net_customer['Name'])
        self.assertEqual(player.Surname, q_net_customer['Surname'])

    def test_tc_2_player_registration_id_41_chars(self):
        player = create_random_player(player_id_length=41)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'PlayerID too long')

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertFalse(q_net_customer)
        self.assertFalse(q_net_dw_fact_signup)

    def test_tc_3_player_registration_empty_email(self):
        player = create_random_player()
        player.Email = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'Email not being passed or is invalid')

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertFalse(q_net_customer)
        self.assertFalse(q_net_dw_fact_signup)

    def test_tc_4_player_registration_invalid_email(self):
        player = create_random_player()
        player.Email = '12345.com'
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'Email not being passed or is invalid')

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertFalse(q_net_customer)
        self.assertFalse(q_net_dw_fact_signup)

    def test_tc_5_player_registration_empty_name(self):
        player = create_random_player()
        player.Name = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)

    def test_tc_6_player_registration_empty_surname(self):
        player = create_random_player()
        player.Surname = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)

    def test_tc_7_player_registration_empty_country_code(self):
        player = create_random_player()
        player.CountryCode = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body['Success'])

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer == [])
        self.assertTrue(q_net_dw_fact_signup == [])

    def test_tc_8_player_registration_empty_city(self):
        player = create_random_player()
        player.City = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")
