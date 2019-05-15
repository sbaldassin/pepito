import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.event_factory import create_parimutuel_event

from tests.utils.utils import get_api_headers, get_api_ok_message, get_dim_parimutuel_resource
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class EventsParimutuelTestCase(TestCase):

    def setUp(self):
        super(EventsParimutuelTestCase, self)

    @retry(Exception)
    def verify_wager_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'], error)
    
    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=100)

    def get_event(self, event_id):
        url = "http://{}/games/parimutuel?event_id={}".format(get_config().get("test_framework", "db"), event_id)
        return get_until_not_empty(url, timeout=100)

    def test_tc_1_create_event_parimutuel_example(self):
        event = create_parimutuel_event()
        logging.info("Creating event: {}".format(event.__dict__))

        parimutuel_event_response = requests.post(get_dim_parimutuel_resource(),
                                                  data=json.dumps([event.__dict__]),
                                                  headers=get_api_headers())
        self.assertTrue(parimutuel_event_response.status_code, 200)
        body = parimutuel_event_response.json()
        logging.info("Event Parimutuel API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)

        q_net_event_list = self.get_event(event.EventID)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertEqual(e['ExternalEventID'], event.EventID)
            self.assertEqual(e['Event'], event.Event)
            self.assertEqual(e['Breed'], event.Breed)
            self.assertEqual(e['MerchantID'], 11)
            self.assertTrue(e['Breed'])
            self.assertTrue(e['EventDate'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['GameID'])
            #self.assertTrue(e['TimeID'])
