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

    def test_tc_1_a_player_registration_russian(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"Москва"
        player.Surname = u"Москва"
        player.CountryCode = u"RU"
        player.City = u"Москва"
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

    def test_tc_1_a_player_registration_arabic(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"جون"
        player.Surname = u"جون"
        player.CountryCode = u"AS"
        player.City = u"الرياض‎"
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

    def test_tc_1_a_player_registration_french(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"Le jeu du garçon"
        player.Surname = u"Le jeu du garçon"
        player.CountryCode = u"FR"
        player.City = u"Nîmes"
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

    def test_tc_1_a_player_registration_cyrillic(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"Иван"
        player.Surname = u"Суроков"
        player.CountryCode = u"РУ"
        player.City = u"Москва"
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

    def test_tc_1_a_player_registration_greece(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"φδασδαφδσ"
        player.Surname = u"αδσφασδ"
        player.CountryCode = u"ΓΡ"
        player.City = u"Διοσ"
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

    def test_tc_1_a_player_registration_chinese(self):
        player = create_random_player(player_id_length=40)
        player.Name = u"凯文"
        player.Surname = u"牡鹿"
        player.CountryCode = u"CZ"
        player.City = u"北京"
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

    def test_tc_22_player_registration_empty_custom_string_1(self):
        player = create_random_player()
        player.CustomString1 = ''
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
        self.assertEquals(q_net_customer["CustomString1"], "")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_23_player_registration_empty_custom_string_2(self):
        player = create_random_player()
        player.CustomString2 = ''
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
        self.assertEquals(q_net_customer["CustomString2"], "")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_24_player_registration_empty_custom_string_3(self):
        player = create_random_player()
        player.CustomString3 = ''
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
        self.assertEquals(q_net_customer["CustomString3"], "")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_24_A_player_registration_empty_custom_string_3_empty_promo_code(self):
        player = create_random_player()
        player.CustomString3 = ''
        player.PromoCode = ''
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
        self.assertEquals(q_net_customer["CustomString3"], player.TrackingCode)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_25_player_registration_empty_custom_string_4(self):
        """
        IMPORTANT NOTE from asana: If the CustomString4 is empty,
        the value from the PromoCode field will be added - IT IS RESERVED FIELD.
        :return:
        """
        player = create_random_player()
        player.CustomString4 = ''
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__), headers=get_api_headers())
        self.assertTrue(response.status_code, 200)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomString4"], player.PromoCode)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_26_player_registration_empty_timezone(self):
        player = create_random_player()
        player.TimeZone = ''
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
        self.assertEquals(q_net_customer["LastKnownTimezone"], "0")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_27_player_registration_zero_as_timezone(self):
        player = create_random_player()
        player.TimeZone = 0
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
        self.assertEquals(q_net_customer["LastKnownTimezone"], "0")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_28_player_registration_empty_language_code(self):
        player = create_random_player()
        player.LanguageCode = ''
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
        self.assertEquals(q_net_customer["LastKnownLanguage"], "")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_29_player_registration_zero_as_language_code(self):
        player = create_random_player()
        player.LanguageCode = 0
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
        self.assertEquals(q_net_customer["LastKnownLanguage"], "0")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_30_player_registration_empty_btag(self):
        player = create_random_player()
        player.Btag = ""
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
        self.assertEquals(q_net_customer["BTag"], "")

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_31_player_registration_empty_promo_code(self):
        """
              IMPORTANT NOTE from asana: If PromoCode the CustomString4 will be replaced with
              promocode value, if promocode is empty CustomString4 will keep it's original value

              :return:
              """
        player = create_random_player()
        player.PromoCode = ""
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
        self.assertEquals(q_net_customer["CustomString4"], str(player.CustomString4))

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_32_player_registration_empty_tracking_code(self):
        """
          IMPORTANT NOTE: According to doc https://qa-gaming.aretonet.com/kb/campaigns#ua_campaigns_promo

          If both a promotional code and a tracking code are received, the promotional code will be taken into
          consideration while the tracking code will be discarded;

          and if tracking code is available this value will be used as CustomString3 iff promo code is not null or empty

          :return:
        """
        player = create_random_player()
        player.TrackingCode = ""
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["CustomString3"], str(player.CustomString3))

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_33_player_registration_empty_optout_email(self):
        player = create_random_player()
        player.OptOutEmail = ""
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutEmail"], False)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_34_player_registration_true_optout_email(self):
        player = create_random_player()
        player.OptOutEmail = True
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutEmail"], True)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_35_player_registration_empty_optout_sms(self):
        player = create_random_player()
        player.OptOutSms = ""
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutSms"], False)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_36_player_registration_true_optout_sms(self):
        player = create_random_player()
        player.OptOutSms = True
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutSms"], True)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_37_player_registration_empty_optout_push(self):
        player = create_random_player()
        player.OptOutPush = ""
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutPush"], False)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    def test_tc_38_player_registration_true_optout_email(self):
        player = create_random_player()
        player.OptOutPush = True
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        self.assertTrue(response.status_code, 500)
        body = response.json()
        logging.info("API response: {}".format(body))

        q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()[0]

        self.assertTrue(q_net_customer)
        self.assertTrue(q_net_dw_fact_signup)
        self.assertEquals(q_net_customer["OptOutPush"], True)

        self.assertTrue(body['Success'])
        self.assertEqual(body["Message"], "OK")

    # BUG optout_mobile_push
    # @skip("No OptoutMobilePush column")
    # def test_tc_39_player_registration_empty_optout_mobile_push(self):
    #     player = create_random_player()
    #     player.OptoutMobilePush = ""
    #     logging.info("Creating player: {}".format(player.__dict__))
    #     response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
    #                              headers=get_api_headers())
    #     self.assertTrue(response.status_code, 500)
    #     body = response.json()
    #     logging.info("API response: {}".format(body))
    #
    #     q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
    #         get_config().get("test_framework", "db"), player.PlayerID)).json()[0]
    #
    #     q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
    #         get_config().get("test_framework", "db"), player.PlayerID)).json()[0]
    #
    #     self.assertTrue(q_net_customer)
    #     self.assertTrue(q_net_dw_fact_signup)
    #     self.assertEquals(q_net_customer["OptoutMobilePush"], "")
    #
    #     self.assertTrue(body['Success'])
    #     self.assertEqual(body["Message"], "OK")

    # BUG optout_mobile_push
    # def test_tc_40_player_registration_true_optout_mobile_push(self):
    #     player = create_random_player()
    #     player.OptoutMobilePush = True
    #     logging.info("Creating player: {}".format(player.__dict__))
    #     response = requests.post(get_player_sign_up_resource(), data=json.dumps(player.__dict__),
    #                              headers=get_api_headers())
    #     self.assertTrue(response.status_code, 500)
    #     body = response.json()
    #     logging.info("API response: {}".format(body))
    #
    #     q_net_customer = requests.get("http://{}/customer?customer_id={}".format(
    #         get_config().get("test_framework", "db"), player.PlayerID)).json()[0]
    #
    #     q_net_dw_fact_signup = requests.get("http://{}/sign_up?customer_id={}".format(
    #         get_config().get("test_framework", "db"), player.PlayerID)).json()[0]
    #
    #     self.assertTrue(q_net_customer)
    #     self.assertTrue(q_net_dw_fact_signup)
    #     self.assertEquals(q_net_customer["OptoutMobilePush"], True)
    #
    #     self.assertTrue(body['Success'])
    #     self.assertEqual(body["Message"], "OK")
