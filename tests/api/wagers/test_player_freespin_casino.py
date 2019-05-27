
import logging
from unittest import TestCase

from tests.config.config import get_config
from tests.factory.freespin_factory import create_freespin
from tests.factory.player_factory import create_random_player

from tests.utils.api_utils import create_areto_api_object, get_freespin_response, verify_api_error
from tests.utils.utils import get_freespin_resource,  get_task_error_invalid_identifier, \
    get_task_error_invalid_value, get_api_error_player_id_not_passed


logging.basicConfig(level=logging.INFO)


class PlayerFreespinCasinoTestCase(TestCase):

    def setUp(self):
        super(PlayerFreespinCasinoTestCase, self)

    def test_tc_1_create_freespin_example(self):
        player = create_random_player(player_id_length=40)
        freespin = create_freespin(is_future=True)
        data = {
            "PlayerID": player.PlayerID,
            "FreeSpins": [freespin.__dict__]
        }

        create_areto_api_object(resource=get_freespin_resource(), data=data)

        q_net_freespin_list = get_freespin_response(data.get('PlayerID'))
        self.assertEqual(len(q_net_freespin_list), 1)

        for e in q_net_freespin_list:
            self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(e['FactFreeSpinID'])
            self.assertTrue(e['TimeID'])
            self.assertTrue(e['SignInID'])
            self.assertTrue(e['FreeSpinID'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['ActivityDate'])
            self.assertEqual(e['ExternalCustomerID'], data['PlayerID'])

    def test_tc_2_create_freespin_without_identifier(self):
        player = create_random_player(player_id_length=40)
        freespin = create_freespin(is_future=True)
        freespin.Identifier = None
        data = {
            "PlayerID": player.PlayerID,
            "FreeSpins": [freespin.__dict__]
        }

        request_id = create_areto_api_object(resource=get_freespin_resource(), data=data)

        verify_api_error(request_id, get_task_error_invalid_identifier())

    def test_tc_3_create_freespin_without_value(self):
        player = create_random_player(player_id_length=40)
        freespin = create_freespin(is_future=True)
        freespin.Value = None
        data = {
            "PlayerID": player.PlayerID,
            "FreeSpins": [freespin.__dict__]
        }

        request_id = create_areto_api_object(resource=get_freespin_resource(), data=data)

        verify_api_error(request_id, get_task_error_invalid_value())

    def test_tc_4_create_freespin_without_transaction_date(self):
        player = create_random_player(player_id_length=40)
        freespin = create_freespin(is_future=True)
        freespin.TransactionDate = None
        data = {
            "PlayerID": player.PlayerID,
            "FreeSpins": [freespin.__dict__]
        }

        create_areto_api_object(resource=get_freespin_resource(), data=data)

        q_net_freespin_list = get_freespin_response(data.get('PlayerID'))
        self.assertEqual(len(q_net_freespin_list), 1)

        for e in q_net_freespin_list:
            self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(e['FactFreeSpinID'])
            self.assertTrue(e['TimeID'])
            #self.assertFalse(e['SignInID'])
            self.assertTrue(e['FreeSpinID'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['ActivityDate'])
            self.assertEqual(e['ExternalCustomerID'], data['PlayerID'])

    # New TC
    def test_tc_5_create_freespin_without_player_id(self):
        freespin = create_freespin(is_future=True)
        data = {
            "FreeSpins": [freespin.__dict__]
        }

        create_areto_api_object(resource=get_freespin_resource(), data=data, success=False,
                                             msg=get_api_error_player_id_not_passed())
