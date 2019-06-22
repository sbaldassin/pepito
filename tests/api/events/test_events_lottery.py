import json
import logging
from unittest import TestCase
import requests

from tests.config.config import get_config
from tests.factory.event_factory import create_lottery_event
from tests.utils.api_utils import get_task

from tests.utils.utils import get_api_headers, get_api_ok_message, get_dim_lottery_resource, \
    get_api_error_event_list_empty, get_task_error_invalid_lottery_event, get_task_error_invalid_breed
from tests.utils.utils import get_task_error_invalid_category
from tests.utils.getters import get_until_not_empty
from tests.utils.retry import retry

logging.basicConfig(level=logging.INFO)


class EventsLotteryTestCase(TestCase):

    def setUp(self):
        super(EventsLotteryTestCase, self)

    @retry(AssertionError, tries=5, delay=5, backoff=2)
    def verify_event_error(self, request_id, error):
        task = self.get_task(request_id)
        self.assertEqual(len(task), 1)
        self.assertEqual(task[0]['Error'].lower(), error.lower())
    
    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_not_empty(url, timeout=100)

    @retry(Exception, tries=5)
    def verify_error(self, request_id, error_message):
        task = self.get_task(request_id)[0]
        logging.info("Task: {}".format(task))
        self.assertFalse(task["Error"] == error_message)

    def get_event(self, name, category):
        url = "http://{}/games/lottery?name={}&category={}".format(
            get_config().get("test_framework", "db"), name, category)
        logging.info("Url: {}".format(url))
        return get_until_not_empty(url, timeout=100)

    def send_lottery_event(self, events):
        parimutuel_event_response = requests.post(get_dim_lottery_resource(),
                                                  data=json.dumps(events),
                                                  headers=get_api_headers())
        self.assertTrue(parimutuel_event_response.status_code, 200)
        body = parimutuel_event_response.json()
        logging.info("Event Parimutuel API response: {}".format(body))
        self.assertEqual(body.get('Success'), True)
        self.assertEqual(body.get('Message'), get_api_ok_message())
        request_id = body.get('RequestID')
        self.assertTrue(request_id)
        return request_id

    def test_tc_1_create_event_lottery_example(self):
        event = create_lottery_event(is_future=True)
        logging.info("Creating event: {}".format(event.__dict__))

        task_id = self.send_lottery_event([event.__dict__])
        task = get_task(task_id)
        logging.info("Task: {}".format(task))

        q_net_event_list = self.get_event(event.Name, event.Category)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertEqual(e['Name'], event.Name)
            self.assertEqual(e['Category'], event.Category)
            self.assertEqual(e['MerchantID'], 11)
            self.assertTrue(e['DrawDate'])
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['GameID'])
            self.assertTrue(e['TimeID'])

    def test_tc_2_create_event_lottery_without_name(self):
        event = create_lottery_event(is_future=True)
        event.Name = None
        logging.info("Creating event: {}".format(event.__dict__))

        request_id = self.send_lottery_event([event.__dict__])

        self.verify_event_error(request_id, get_task_error_invalid_lottery_event())

    def test_tc_3_create_event_lottery_without_category(self):
        """
        The TC in asana is not correct, basically it states that the event should be created
        becasue category is optional, but according to the doc, category is a required param,
        and also the expected result in this case is to get an error: Invalid Category on record number 1. No data saved.
        """
        event = create_lottery_event(is_future=True)
        event.Category = None
        logging.info("Creating event: {}".format(event.__dict__))

        request_id = self.send_lottery_event([event.__dict__])

        q_net_event_list = self.get_event(event.Name, '')
        self.assertEqual(len(q_net_event_list), 0)
        self.verify_error(request_id, get_task_error_invalid_category())

    def test_tc_4_create_event_lottery_without_draw_date(self):
        event = create_lottery_event(is_future=True)
        event.DrawDate = None
        logging.info("Creating event: {}".format(event.__dict__))

        self.send_lottery_event([event.__dict__])

        q_net_event_list = self.get_event(event.Name, event.Category)
        self.assertEqual(len(q_net_event_list), 1)

        for e in q_net_event_list:
            self.assertEqual(e['Name'], event.Name)
            self.assertEqual(e['Category'], event.Category)
            self.assertEqual(e['MerchantID'], 11)
            self.assertEqual(e['DrawDate'], None)
            self.assertTrue(e['DateCreated'])
            self.assertTrue(e['GameID'])
            self.assertEqual(e['TimeID'], 0)

    def test_tc_5_create_event_lottery_aggregated(self):
        events = []
        for i in range(2):
            events.append(create_lottery_event(is_future=True).__dict__)

        self.send_lottery_event(events)

        for event in events:
            q_net_event_list = self.get_event(event['Name'], event['Category'])
            self.assertEqual(len(q_net_event_list), 1)

            for e in q_net_event_list:
                self.assertEqual(e['Name'], event['Name'])
                self.assertEqual(e['Category'], event['Category'])
                self.assertEqual(e['MerchantID'], 11)
                self.assertTrue(e['DrawDate'])
                self.assertTrue(e['DateCreated'])
                self.assertTrue(e['GameID'])
                self.assertTrue(e['TimeID'])

    # New tc
    def test_tc_6_event_lottery_empty_list(self):
        parimutuel_event_response = requests.post(get_dim_lottery_resource(),
                                                  data=json.dumps([]),
                                                  headers=get_api_headers())
        self.assertTrue(parimutuel_event_response.status_code, 200)
        body = parimutuel_event_response.json()
        self.assertEqual(body.get('Success'), False)
        self.assertEqual(body.get('Message'), get_api_error_event_list_empty())
        self.assertEqual(body.get('RequestID'), 0)
