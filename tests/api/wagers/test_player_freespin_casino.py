import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.freespin_factory import create_freespin

from tests.utils.api_utils import create_areto_api_object, get_freespin_response
from tests.utils.utils import get_api_headers, get_api_ok_message, get_freespin_resource, \
    get_api_error_event_list_empty, get_task_error_invalid_sport_event, get_task_error_invalid_sport_league, \
    get_task_error_invalid_parimutuel_event
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class PlayerFreespinCasinoTestCase(TestCase):

    def setUp(self):
        super(PlayerFreespinCasinoTestCase, self)

    @retry(AssertionError, tries=5, delay=5, backoff=2)
    def verify_event_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'].lower(), error.lower())

    def test_tc_1_create_freespin_example(self):
        freespin = create_freespin(is_future=True)
        data = {
            "PlayerID": "1231231T",
            "InitID": 15401920,
            "FreeSpins": [freespin.__dict__]
        }

        create_areto_api_object(resource=get_freespin_resource(), data=data)

        q_net_freespin_list = get_freespin_response(data.get('PlayerID'))
        self.assertEqual(len(q_net_freespin_list), 1)

        for e in q_net_freespin_list:
            self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
            self.assertTrue(e['FactFreeSpinID'])
            self.assertTrue(e['TimeID'])
            self.assertTrue(e['FreeSpinID'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['ActivityDate'])
            self.assertEqual(e['ExternalCustomerID'], data['PlayerID'])
    #
    # def test_tc_2_create_event_sport_without_sport(self):
    #     event = create_sport_event(is_future=True)
    #     event.Sport = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     request_id = self.send_sport_event([event.__dict__])
    #
    #     self.verify_event_error(request_id, get_task_error_invalid_sport_event())
    #
    # def test_tc_3_create_event_sport_without_league(self):
    #     event = create_sport_event(is_future=True)
    #     event.League = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     request_id = self.send_sport_event([event.__dict__])
    #
    #     self.verify_event_error(request_id, get_task_error_invalid_sport_league())
    #
    # def test_tc_4_create_event_sport_without_event(self):
    #     event = create_sport_event(is_future=True)
    #     event.Event = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     request_id = self.send_sport_event([event.__dict__])
    #
    #     self.verify_event_error(request_id, get_task_error_invalid_parimutuel_event())
    #
    # def test_tc_5_create_event_sport_without_live(self):
    #     event = create_sport_event(is_future=True)
    #     event.Live = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     self.send_sport_event([event.__dict__])
    #
    #     q_net_event_list = self.get_event(event.EventID)
    #     self.assertEqual(len(q_net_event_list), 1)
    #
    #     for e in q_net_event_list:
    #         self.assertEqual(e['Event'], event.Event)
    #         self.assertTrue(e['TimeID'])
    #         self.assertTrue(e['GameID'])
    #         self.assertFalse(e['Live'])
    #         self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
    #         self.assertTrue(e['DateCreated'])
    #         self.assertTrue(e['EventDate'])
    #         self.assertEqual(e['Sport'], event.Sport)
    #         self.assertEqual(e['ExternalEventID'], event.EventID)
    #         self.assertEqual(e['League'], event.League)
    #
    # def test_tc_6_create_event_sport_without_event_date(self):
    #     event = create_sport_event(is_future=True)
    #     event.EventDate = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     self.send_sport_event([event.__dict__])
    #
    #     q_net_event_list = self.get_event(event.EventID)
    #     self.assertEqual(len(q_net_event_list), 1)
    #
    #     for e in q_net_event_list:
    #         self.assertEqual(e['Event'], event.Event)
    #         self.assertEqual(e['TimeID'], 0)
    #         self.assertTrue(e['GameID'])
    #         self.assertEqual(e['Live'], event.Live)
    #         self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
    #         self.assertTrue(e['DateCreated'])
    #         self.assertEqual(e['EventDate'], None)
    #         self.assertEqual(e['Sport'], event.Sport)
    #         self.assertEqual(e['ExternalEventID'], event.EventID)
    #         self.assertEqual(e['League'], event.League)
    #
    # def test_tc_7_create_event_sport_without_event_id(self):
    #     event = create_sport_event(is_future=True)
    #     event.EventID = None
    #     logging.info("Creating event: {}".format(event.__dict__))
    #
    #     self.send_sport_event([event.__dict__])
    #
    #     q_net_event_list = self.get_event(event.EventID, event.Event)
    #     self.assertEqual(len(q_net_event_list), 1)
    #
    #     for e in q_net_event_list:
    #         self.assertEqual(e['Event'], event.Event)
    #         self.assertTrue(e['TimeID'])
    #         self.assertTrue(e['GameID'])
    #         self.assertEqual(e['Live'], event.Live)
    #         self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
    #         self.assertTrue(e['DateCreated'])
    #         self.assertTrue(e['EventDate'], None)
    #         self.assertEqual(e['Sport'], event.Sport)
    #         self.assertEqual(e['ExternalEventID'], '')
    #         self.assertEqual(e['League'], event.League)
    #
    # def test_tc_8_create_event_sports_aggregated(self):
    #     events = []
    #     for i in range(2):
    #         events.append(create_sport_event(is_future=True).__dict__)
    #
    #     self.send_sport_event(events)
    #
    #     for event in events:
    #         q_net_event_list = self.get_event(event['EventID'])
    #         self.assertEqual(len(q_net_event_list), 1)
    #
    #         for e in q_net_event_list:
    #             self.assertEqual(e['Event'], event['Event'])
    #             self.assertTrue(e['TimeID'])
    #             self.assertTrue(e['GameID'])
    #             self.assertEqual(e['Live'], event['Live'])
    #             self.assertEqual(e['MerchantID'], int(get_config().get("api", "merchant_id")))
    #             self.assertTrue(e['DateCreated'])
    #             self.assertTrue(e['EventDate'])
    #             self.assertEqual(e['Sport'], event['Sport'])
    #             self.assertEqual(e['ExternalEventID'], event['EventID'])
    #             self.assertEqual(e['League'], event['League'])
    #
    # # New tc
    # def test_tc_9_event_sports_empty_list(self):
    #     parimutuel_event_response = requests.post(get_dim_sports_resource(),
    #                                               data=json.dumps([]),
    #                                               headers=get_api_headers())
    #     self.assertTrue(parimutuel_event_response.status_code, 200)
    #     body = parimutuel_event_response.json()
    #     self.assertEqual(body.get('Success'), False)
    #     self.assertEqual(body.get('Message'), get_api_error_event_list_empty())
    #     self.assertEqual(body.get('RequestID'), 0)
