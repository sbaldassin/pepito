import datetime
import json
import logging
from unittest import TestCase
import requests
from tests.config.config import get_config
from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_bet
from tests.utils.generator import generate_random_int, generate_random_date, generate_random_string
from tests.utils.getters import get_until_not_empty, get_until_attempt_greater_than_zero
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_wager_betting_resource

logging.basicConfig(level=logging.INFO)


class WagerBetTestCase(TestCase):

    def setUp(self):
        super(WagerBetTestCase, self)

    def test_tc_1_player_wager_bet(self):
        player, wager, _ = self._create_player_with_wager()
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])
        self.assertTrue(result[0]["EuroCentsValue"] != 0)

    def test_tc_2_wager_bet_invalid_currency(self):
        wager = create_bet()
        wager.Currency = "Invalid"
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_3_wager_bet_string_amount(self):
        wager = create_bet()
        wager.Value = "value"
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_4_wager_bet_invalid_amount(self):
        wager = create_bet()
        wager.Value = -1
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_5_wager_bet_zero_amount(self):
        wager = create_bet()
        wager.Value = 0
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_6_wager_bet_usd_currency(self):
        wager = create_bet()
        wager.Currency = "USD"
        player, revenue, _ = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        logging.info("DB result: {}".format(result))

        self.assertFalse(result == [])

    def test_tc_7_wager_bet_invalid_transaction_date(self):
        wager = create_bet()
        wager.TransactionDate = "invalid_date"
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_8_wager_bet_future_transaction_date(self):
        wager = create_bet()
        wager.TransactionDate = generate_random_date(is_future=True)
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_9_wager_bet_invalid_count(self):
        wager = create_bet()
        wager.Count = "count"
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_10_wager_bet_zero_count(self):
        wager = create_bet()
        wager.Count = 0
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_11_wager_bet_negative_count(self):
        wager = create_bet()
        wager.Count = -1
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    def test_tc_12_wager_bet_huge_count(self):
        wager = create_bet()
        wager.Count = 100000000000000
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_13_wager_bet_invalid_event_date(self):
        wager = create_bet()
        wager.EventDate = "invalid_date"
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_14_wager_bet_past_event_date(self):
        wager = create_bet()
        wager.EventDate = generate_random_date()
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_15_wager_bet_non_existing_category(self):
        wager = create_bet()
        wager.EventCategory = generate_random_string()
        player, revenue, request_id = self._create_player_with_wager([wager])
        result = self.get_wager_from_db(player)
        self.assertFalse(result == [])

    def test_tc_16_wager_bet_non_existing_event(self):
        wager = create_bet()
        wager.Event = None
        player, revenue, request_id = self._create_player_with_wager([wager])
        self.assert_not_created(request_id, player)

    @staticmethod
    def get_wager_from_db(player):
        url = "http://{}/wagers?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url, timeout=120)

    @staticmethod
    def _create_player():
        player = create_random_player(player_id_length=40)
        logging.info("Creating player: {}".format(player.__dict__))
        response = requests.post(get_player_sign_up_resource(),
                                 data=json.dumps(player.__dict__),
                                 headers=get_api_headers())
        body = response.json()
        logging.info("API response: {}".format(body))
        return player

    @staticmethod
    def _create_wagers(player, wagers=[]):
        _wagers = [create_bet()] if wagers == [] else wagers
        logging.info("Creating wagers: {}".format([r.__dict__ for r in _wagers]))

        data = {"PlayerID": player.PlayerID, "InitID": generate_random_int(),
                "Wagers": [r.__dict__ for r in _wagers]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_wager_betting_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return wagers, response.json()["RequestID"]

    def _create_player_with_wager(self, wagers=[]):
        player = self._create_player()
        wagers, request_id = self._create_wagers(player, wagers)
        return player, wagers, request_id

    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_attempt_greater_than_zero(url, timeout=80)

    def assert_not_created(self, request_id, player):
        try:
            task = self.get_task(request_id)[0]
            logging.info("Task: {}".format(task))
            self.assertFalse(task["Error"] == "")
        except IndexError:
            result = self.get_wager_from_db(player)
            logging.info("DB result: {}".format(result))
            self.assertTrue(result == [])
