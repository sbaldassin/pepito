import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_api_headers, get_player_sign_up_resource, get_player_update_resource, get_api_ok_message

logging.basicConfig(level=logging.INFO)


class PlayerUpdateTestCase(TestCase):

    def setUp(self):
        super(PlayerUpdateTestCase, self)
    
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
        return q_net_customer

    def update_and_validate_player(self, player, obj_field, db_field):
        player_update_response = requests.post(get_player_update_resource(), data=json.dumps(player.__dict__),
                                               headers=get_api_headers())
        self.assertTrue(player_update_response.status_code, 200)
        body = player_update_response.json()
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        updated_q_net_customer_list = self.get_customer(player)
        updated_q_net_customer = [c for c in updated_q_net_customer_list if getattr(player, obj_field) == c[db_field]]
        
        self.assertTrue(updated_q_net_customer)
        return updated_q_net_customer[0]

    def get_signup(self, player):
        return requests.get("http://{}/sign_up?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()

    def get_customer(self, player):
        return requests.get("http://{}/customer?customer_id={}".format(
            get_config().get("test_framework", "db"), player.PlayerID)).json()
    
    def test_tc_1_player_id_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
        
        # Create player
        self.create_and_validate_player(player)

        # Update player
        player.PlayerID = player.PlayerID + player.PlayerID[-1]
        self.update_and_validate_player(player, 'PlayerID', 'ExternalCustomerID')

    def test_tc_2_email_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['Email'], player.Email)
    
        # Update player
        player.Email = player.Email + player.Email[-1]
        self.update_and_validate_player(player, 'Email', 'Email')

    def test_tc_3_name_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['Name'], player.Name)
    
        # Update player
        player.Name = player.Name + player.Name[-1]
        self.update_and_validate_player(player, 'Name', 'Name')

    def test_tc_4_surname_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['Surname'], player.Surname)
    
        # Update player
        player.Surname = player.Surname + player.Surname[-1]
        self.update_and_validate_player(player, 'Surname', 'Surname')

    def test_tc_5_country_code_and_city_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['City'], player.City)
        self.assertEqual(q_net_customer['CountryCode'], player.CountryCode)
        
    
        # Update player
        player.CountryCode = '{}{}'.format(player.CountryCode[1], player.CountryCode[0])
        player.City = player.City + player.City[-1]
        updated_q_net_customer = self.update_and_validate_player(player, 'CountryCode', 'CountryCode')
        self.assertEqual(player.City, updated_q_net_customer['City'])

    def test_tc_6_zipcode_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['ZipCode'], player.ZipCode)
    
        # Update player
        player.ZipCode = player.ZipCode + player.ZipCode[-1]
        self.update_and_validate_player(player, 'ZipCode', 'ZipCode')

    def test_tc_7_state_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['State'], player.State)
    
        # Update player
        player.State = player.State + player.State[-1]
        self.update_and_validate_player(player, 'State', 'State')

    def test_tc_8_mobilephone_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['PhoneNumber'], player.MobilePhone)
    
        # Update player
        player.MobilePhone = player.MobilePhone + player.MobilePhone[-1]
        self.update_and_validate_player(player, 'MobilePhone', 'PhoneNumber')

    def test_tc_9_custom_string1_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['CustomString1'], player.CustomString1)
    
        # Update player
        player.CustomString1 = player.CustomString1 + player.CustomString1[-1]
        self.update_and_validate_player(player, 'CustomString1', 'CustomString1')

    def test_tc_10_custom_string2_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['CustomString2'], player.CustomString2)
    
        # Update player
        player.CustomString2 = player.CustomString2 + player.CustomString2[-1]
        self.update_and_validate_player(player, 'CustomString2', 'CustomString2')

    def test_tc_11_custom_string3_update(self):
        player = create_random_player(player_id_length=30)
        logging.info("Creating player: {}".format(player.__dict__))
    
        # Create player
        q_net_customer = self.create_and_validate_player(player)
        self.assertEqual(q_net_customer['CustomString1'], player.CustomString1)
    
        # Update player
        player.CustomString3 = player.CustomString3 + player.CustomString3[-1]
        self.update_and_validate_player(player, 'CustomString3', 'CustomString3')

