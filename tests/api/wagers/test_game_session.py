
import logging
from unittest import TestCase

from tests.config.config import get_config
from tests.factory.game_session_factory import create_game_session
from tests.factory.player_factory import create_random_player

from tests.utils.api_utils import create_areto_api_object, get_game_session_response, verify_api_error
from tests.utils.utils import get_game_session_resource,  get_task_error_invalid_identifier, \
    get_task_error_invalid_value, get_api_error_player_id_not_passed


logging.basicConfig(level=logging.INFO)


class GameSessionTestCase(TestCase):

    def setUp(self):
        super(GameSessionTestCase, self)

    def test_tc_1_create_game_session_casino(self):
        player = create_random_player(player_id_length=40)
        session = create_game_session()
        data = {
            "PlayerID": player.PlayerID,
            "GameSessions": [session.__dict__]
        }
        channel = 1
        import pdb; pdb.set_trace()
        create_areto_api_object(resource=get_game_session_resource(channel), data=session_request.__dict__)

        for session in data['GameSessions']:
            q_net_session_list = get_game_session_response(player.PlayerID)
            self.assertEqual(len(q_net_session_list['fact']), 1)
            self.assertEqual(len(q_net_session_list['dim']), 1)

            for e in q_net_session_list:

                self.assertEqual(e['fact']['MerchantID'], int(get_config().get("api", "merchant_id")))
                self.assertTrue(e['fact']['ActivityDate'])
                self.assertTrue(e['fact']['DateCreated'])
                self.assertTrue(e['fact']['ExternalCustomerID'], player.PlayerID)
                self.assertTrue(e['fact']['ChannelID'], channel)
                self.assertTrue(e['fact']['FactGameID'])
                self.assertTrue(e['fact']['GameID'])
                self.assertTrue(e['fact']['TimeID'])
                game_id = e['fact']['GameID']
                self.assertEqual(e['dim']['MerchantID'], int(get_config().get("api", "merchant_id")))
                self.assertTrue(e['dim']['DateCreated'])
                self.assertEqual(e['dim']['GameName'], session.GameIdentifier)
                self.assertEqual(e['dim']['GameCategory'], session.GameType)
                self.assertEqual(e['dim']['GameID'], game_id)

    # def test_tc_2_create_freespin_without_identifier(self):
    #     player = create_random_player(player_id_length=40)
    #     freespin = create_freespin(is_future=True)
    #     freespin.Identifier = None
    #     data = {
    #         "PlayerID": player.PlayerID,
    #         "FreeSpins": [freespin.__dict__]
    #     }
    #
    #     request_id = create_areto_api_object(resource=get_freespin_resource(), data=data)
    #
    #     verify_api_error(request_id, get_task_error_invalid_identifier())
    #
    # def test_tc_3_create_freespin_without_value(self):
    #     player = create_random_player(player_id_length=40)
    #     freespin = create_freespin(is_future=True)
    #     freespin.Value = None
    #     data = {
    #         "PlayerID": player.PlayerID,
    #         "FreeSpins": [freespin.__dict__]
    #     }
    #
    #     request_id = create_areto_api_object(resource=get_freespin_resource(), data=data)
    #
    #     verify_api_error(request_id, get_task_error_invalid_value())
    #
    # def test_tc_4_create_freespin_without_transaction_date(self):
    #     player = create_random_player(player_id_length=40)
    #     freespin = create_freespin(is_future=True)
    #     freespin.TransactionDate = None
    #     data = {
    #         "PlayerID": player.PlayerID,
    #         "FreeSpins": [freespin.__dict__]
    #     }
    #
    #     create_areto_api_object(resource=get_freespin_resource(), data=data)
    #
    #     q_net_freespin_list = get_freespin_response(data.get('PlayerID'))
    #     self.assertEqual(len(q_net_freespin_list), 1)
    #
    #     for e in q_net_freespin_list:
    #         self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
    #         self.assertTrue(e['FactFreeSpinID'])
    #         self.assertTrue(e['TimeID'])
    #         #self.assertFalse(e['SignInID'])
    #         self.assertTrue(e['FreeSpinID'])
    #         self.assertTrue(e['DateCreated'])
    #         self.assertTrue(e['ActivityDate'])
    #         self.assertEqual(e['ExternalCustomerID'], data['PlayerID'])
    #
    # # New TC
    # def test_tc_5_create_freespin_without_player_id(self):
    #     freespin = create_freespin(is_future=True)
    #     data = {
    #         "FreeSpins": [freespin.__dict__]
    #     }
    #
    #     create_areto_api_object(resource=get_freespin_resource(), data=data, success=False,
    #                                          msg=get_api_error_player_id_not_passed())
