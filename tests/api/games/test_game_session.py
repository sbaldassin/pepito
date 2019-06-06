
import logging
from unittest import TestCase

from tests.config.config import get_config
from tests.factory.game_session_factory import create_game_session
from tests.factory.player_factory import create_random_player

from tests.utils.api_utils import create_areto_api_object, get_game_session_response, verify_api_error
from tests.utils.utils import get_game_session_resource,  get_task_error_invalid_game_type, get_task_error_invalid_game_identifier


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
        create_areto_api_object(resource=get_game_session_resource(channel), data=data)
        for session in data['GameSessions']:
            q_net_session_list = get_game_session_response(player.PlayerID)
            self.assertEqual(len(q_net_session_list['fact']), 1)
            self.assertEqual(len(q_net_session_list['dim']), 1)
            fact = q_net_session_list['fact'][0]
            self.assertEqual(fact['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(fact['ActivityDate'])
            self.assertTrue(fact['DateCreated'])
            self.assertTrue(fact['ExternalCustomerID'], player.PlayerID)
            self.assertTrue(fact['ChannelID'], channel)
            self.assertTrue(fact['FactGameID'])
            self.assertTrue(fact['GameID'])
            self.assertGreaterEqual(fact['TimeID'], 0)
            self.assertGreaterEqual(fact['SignInID'], 0)
            game_id = fact['GameID']
            dim = q_net_session_list['dim'][0]
            self.assertEqual(dim['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(dim['DateCreated'])
            self.assertEqual(dim['GameName'], session['GameIdentifier'])
            self.assertEqual(dim['GameCategory'], session['GameType'])
            self.assertEqual(dim['GameID'], game_id)

    def test_tc_2_game_session_casion_without_game_type(self):
        player = create_random_player(player_id_length=40)
        session = create_game_session()
        session.GameType = None
        data = {
            "PlayerID": player.PlayerID,
            "GameSessions": [session.__dict__]
        }

        request_id = create_areto_api_object(resource=get_game_session_resource(), data=data)

        verify_api_error(request_id, get_task_error_invalid_game_type())

    def test_tc_3_game_session_casion_without_game_identifier(self):
        player = create_random_player(player_id_length=40)
        session = create_game_session()
        session.GameIdentifier = None
        data = {
            "PlayerID": player.PlayerID,
            "GameSessions": [session.__dict__]
        }

        request_id = create_areto_api_object(resource=get_game_session_resource(), data=data)

        verify_api_error(request_id, get_task_error_invalid_game_identifier())

    def test_tc_4_create_game_session_casino_without_session_date(self):
        player = create_random_player(player_id_length=40)
        session = create_game_session()
        session.SessionDate = None
        data = {
            "PlayerID": player.PlayerID,
            "GameSessions": [session.__dict__]
        }
        channel = 1
        create_areto_api_object(resource=get_game_session_resource(channel), data=data)
        for session in data['GameSessions']:
            q_net_session_list = get_game_session_response(player.PlayerID)
            self.assertEqual(len(q_net_session_list['fact']), 1)
            self.assertEqual(len(q_net_session_list['dim']), 1)
            fact = q_net_session_list['fact'][0]
            self.assertEqual(fact['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(fact['ActivityDate'])
            self.assertTrue(fact['DateCreated'])
            self.assertTrue(fact['ExternalCustomerID'], player.PlayerID)
            self.assertTrue(fact['ChannelID'], channel)
            self.assertTrue(fact['FactGameID'])
            self.assertTrue(fact['GameID'])
            self.assertGreaterEqual(fact['TimeID'], 0)
            self.assertGreaterEqual(fact['SignInID'], 0)
            game_id = fact['GameID']
            dim = q_net_session_list['dim'][0]
            self.assertEqual(dim['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(dim['DateCreated'])
            self.assertEqual(dim['GameName'], session['GameIdentifier'])
            self.assertEqual(dim['GameCategory'], session['GameType'])
            self.assertEqual(dim['GameID'], game_id)
