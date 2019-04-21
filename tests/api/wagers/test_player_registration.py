import json
import logging
from unittest import TestCase, skip
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
            get_config().get("test_framework", "db"), player.PlayerID)).json()

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

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer['City'], player.City)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_9_player_registration_empty_zip_code(self):
        player = create_random_player()
        player.ZipCode = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer['ZipCode'], player.ZipCode)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    @skip("Customers table does not have a state column yet")
    def test_tc_10_player_registration_empty_state(self):
        player = create_random_player()
        player.State = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer['State'], player.State)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_11_player_registration_empty_mobile(self):
        player = create_random_player()
        player.MobilePhone = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer['PhoneNumber'], player.MobilePhone)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_12_player_registration_empty_signup_date(self):
        player = create_random_player()
        player.SignUpDate = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertNotEquals(q_net_dw_fact_signup['SignUpDate'], player.SignUpDate)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_13_player_registration_empty_date_of_birth(self):
        player = create_random_player()
        player.DateOfBirth = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals("1900-01-01", q_net_customer['DateOfBirth'])

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_14_player_registration_empty_custom_int_1(self):
        player = create_random_player()
        player.CustomInt1 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt1"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_15_player_registration_string_in_custom_int_1(self):
        player = create_random_player()
        player.CustomInt1 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt1"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_16_player_registration_empty_custom_int_2(self):
        player = create_random_player()
        player.CustomInt2 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt2"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_17_player_registration_string_custom_int_2(self):
        player = create_random_player()
        player.CustomInt2 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt2"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_18_player_registration_empty_custom_int_3(self):
        player = create_random_player()
        player.CustomInt3 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt3"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_19_player_registration_string_custom_int_3(self):
        player = create_random_player()
        player.CustomInt3 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt3"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_20_player_registration_empty_custom_int_4(self):
        player = create_random_player()
        player.CustomInt4 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt4"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_21_player_registration_string_custom_int_4(self):
        player = create_random_player()
        player.CustomInt4 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomInt4"], 0)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")