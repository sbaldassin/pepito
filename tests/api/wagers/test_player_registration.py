import json
import logging
from unittest import TestCase
import requests

from tests.db.mssql_driver import MsSqlDriver
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource

logging.basicConfig(level=logging.INFO)


class PlayerRegistrationTestCase(TestCase):

    def test_tc_1_player_registration_id_40_chars(self):
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertIsNotNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNotNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_2_player_registration_id_41_chars(self):
        player = create_random_player(player_id_length=41)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'PlayerID too long')
        self.assertIsNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_3_player_registration_empty_email(self):
        player = create_random_player()
        player.Email = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'Email not being passed or is invalid')
        self.assertIsNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_4_player_registration_invalid_email(self):
        player = create_random_player()
        player.Email = '12345.com'
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body.get('Success'))
        self.assertTrue(body.get('Message'), 'Email not being passed or is invalid')
        self.assertIsNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_5_player_registration_empty_name(self):
        player = create_random_player()
        player.Name = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertIsNotNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNotNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_6_player_registration_empty_surname(self):
        player = create_random_player()
        player.Surname = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertTrue(body.get('Success'), True)
        self.assertIsNotNone(MsSqlDriver().get_player_from_customer(player))
        self.assertIsNotNone(MsSqlDriver().get_player_from_fact_signup(player))

    def test_tc_7_player_registration_empty_country_code(self):
        player = create_random_player()
        player.CountryCode = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body['Success'])
        self.assertEqual(body["Message"], "CountryCode not being passed or is invalid")

    def test_tc_8_player_registration_empty_city(self):
        player = create_random_player()
        player.City = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))
        self.assertFalse(body['Success'])
        self.assertEqual(body["Message"], "CountryCode not being passed or is invalid")