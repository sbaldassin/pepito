import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.event_factory import create_sport_event

from tests.utils.utils import get_api_headers, get_api_ok_message, get_dim_sports_resource, \
    get_api_error_event_list_empty, get_task_error_invalid_parimutuel_event, get_task_error_invalid_breed
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class EventsSportsTestCase(TestCase):

    def setUp(self):
        super(EventsSportsTestCase, self)

    @retry(AssertionError, tries=5, delay=5, backoff=2)
    def verify_event_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'].lower(), error.lower())
    
    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=100)

    def get_event(self, event_id):
        url = "http://{}/games/sports?event_id={}".format(get_config().get("test_framework", "db"), event_id)
        return get_until_not_empty(url, timeout=100)

    def send_sport_event(self, events):
        parimutuel_event_response = requests.post(get_dim_sports_resource(),
                                                  data=json.dumps(events),
                                                  headers=get_api_headers())
        self.assertTrue(parimutuel_event_response.status_code, 200)
        body = parimutuel_event_response.json()
        logging.info("Event Sports API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)
        return request_id

    def test_tc_1_create_event_sports_example(self):
        event = create_sport_event(is_future=True)
        logging.info("Creating event: {}".format(event.__dict__))

        self.send_sport_event([event.__dict__])

        q_net_event_list = self.get_event(event.EventID)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertEqual(e['Event'], event.Event)
            self.assertTrue(e['TimeID'])
            self.assertTrue(e['GameID'])
            self.assertEqual(e['Live'], event.Live)
            self.assertEqual(e['MerchantID'], get_config().get("api", "merchant_id"))
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['EventDate'])
            self.assertEqual(e['Sport'], event.Sport)
            self.assertEqual(e['ExternalEventID'], event.EventID)
            self.assertEqual(e['League'], event.League)

    def atest_tc_2_create_event_parimutuel_without_event(self):
        event = create_sport_event(is_future=True)
        event.Event = None
        logging.info("Creating event: {}".format(event.__dict__))

        request_id = self.send_sport_event([event.__dict__])

        self.verify_event_error(request_id, get_task_error_invalid_parimutuel_event())

    def atest_tc_3_create_event_parimutuel_without_breed(self):
        event = create_sport_event(is_future=True)
        event.Breed = None
        logging.info("Creating event: {}".format(event.__dict__))

        request_id = self.send_sport_event([event.__dict__])

        self.verify_event_error(request_id, get_task_error_invalid_breed())

    def atest_tc_4_create_event_parimutuel_without_event_date(self):
        event = create_sport_event(is_future=True)
        event.EventDate = None
        logging.info("Creating event: {}".format(event.__dict__))

        self.send_sport_event([event.__dict__])

        q_net_event_list = self.get_event(event.EventID)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertEqual(e['ExternalEventID'], event.EventID)
            self.assertEqual(e['Event'], event.Event)
            self.assertEqual(e['Breed'], event.Breed)
            self.assertEqual(e['MerchantID'], 11)
            self.assertTrue(e['Breed'])
            self.assertEqual(e['EventDate'], None)
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['GameID'])
            self.assertEqual(e['TimeID'], 0)

    def atest_tc_5_create_event_parimutuel_without_event_id(self):
        event = create_sport_event(is_future=True)
        event.EventID = None
        logging.info("Creating event: {}".format(event.__dict__))

        self.send_sport_event([event.__dict__])

        q_net_event_list = self.get_event_by_breed(event.Breed)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertFalse(e['ExternalEventID'])
            self.assertEqual(e['Event'], event.Event)
            self.assertEqual(e['Breed'], event.Breed)
            self.assertEqual(e['MerchantID'], 11)
            self.assertTrue(e['Breed'])
            self.assertTrue(e['EventDate'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['GameID'])

    def atest_tc_6_create_event_parimutuel_aggregated(self):
        events = []
        for i in range(2):
            events.append(create_sport_event(is_future=True).__dict__)

        self.send_sport_event(events)

        for event in events:
            q_net_event_list = self.get_event(event['EventID'])
            self.assertEqual(len(q_net_event_list), 1)

            for e in q_net_event_list:
                self.assertEqual(e['ExternalEventID'], event['EventID'])
                self.assertEqual(e['Event'], event['Event'])
                self.assertEqual(e['Breed'], event['Breed'])
                self.assertEqual(e['MerchantID'], 11)
                self.assertTrue(e['Breed'])
                self.assertTrue(e['EventDate'])
                self.assertTrue(e['DateCreated'])
                self.assertTrue(e['GameID'])
                self.assertTrue(e['TimeID'])

    # New tc
    def atest_tc_7_event_parimutuel_empty_list(self):
        parimutuel_event_response = requests.post(get_dim_sports_resource(),
                                                  data=json.dumps([]),
                                                  headers=get_api_headers())
        self.assertTrue(parimutuel_event_response.status_code, 200)
        body = parimutuel_event_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_event_list_empty())
        self.assertEqual(body.get('RequestID'), 0)
