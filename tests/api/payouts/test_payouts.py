import json
import logging
from unittest import TestCase

import requests

from tests.config.config import get_config
from tests.factory.payout_factory import create_payout
from tests.factory.player_factory import create_random_player

from tests.utils.generator import generate_random_int, generate_random_date
from tests.utils.getters import get_until_not_empty, get_until_attempt_greater_than_zero
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_payout_resource

logging.basicConfig(level=logging.INFO)


class PayoutTestCase(TestCase):

    def setUp(self):
        super(PayoutTestCase, self)

    def test_tc_1_player_payout_casino(self):
        player, payout, _ = self._create_player_with_payout(payout_type="casino")
        self.assert_created(player)

    def test_tc_2_player_payout_sport(self):
        player, payout, _ = self._create_player_with_payout(payout_type="sport")
        self.assert_created(player)

    def test_tc_3_player_payout_bet(self):
        player, payout, _ = self._create_player_with_payout(payout_type="bet")
        self.assert_created(player)

    def test_tc_4_player_payout_esport(self):
        player, payout, _ = self._create_player_with_payout(payout_type="esport")
        self.assert_created(player)

    def test_tc_5_player_payout_lottery(self):
        player, payout, _ = self._create_player_with_payout(payout_type="lottery")
        self.assert_created(player)

    def test_tc_6_player_payout_parimutuel(self):
        player, payout, _ = self._create_player_with_payout(payout_type="parimutuel")
        self.assert_created(player)

    def test_tc_7_player_payout_with_invalid_currency(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Currency = "pepe"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")

        self.assert_not_created(request_id)

    def test_tc_8_player_payout_with_string_amount(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Amount = "pepe"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")

        self.assert_not_created(request_id)

    def test_tc_9_player_payout_with_zero_amount(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Amount = 0
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")

        self.assert_not_created(request_id)

    def test_tc_10_player_payout_with_negative_amount(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Amount = -1
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_created(player)

    def test_tc_11_player_payout_with_huge_amount(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Amount = 1000000000000000000000000000000000000000
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_12_player_payout_with_invalid_game(self):
        payout = create_payout(payout_type="parimutuel")
        payout.ProductID = 10
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_13_player_payout_without_game(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game = {}
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_14_player_payout_with_usd_currency(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Currency = "USD"
        player, payout, _ = self._create_player_with_payout(payouts=[payout],
                                                            payout_type="casino")
        self.assert_created(player)

    def test_tc_15_player_payout_zero_count(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Count = 0
        player, payout, _ = self._create_player_with_payout(payouts=[payout],
                                                            payout_type="casino")
        self.assert_created(player)

    def test_tc_16_player_payout_with_negative_count(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['Count'] = -1
        player, payout, _ = self._create_player_with_payout(payouts=[payout],
                                                            payout_type="casino")
        self.assert_created(player)

    def test_tc_17_player_payout_with_string_count(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Count = "pepe"
        player, payout, _ = self._create_player_with_payout(payouts=[payout],
                                                            payout_type="casino")
        self.assert_created(player)

    def test_tc_18_player_payout_with_invalid_transaction_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.TransactionDate = "pepe"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_created(player)

    def test_tc_19_player_payout_with_future_transaction_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.TransactionDate = generate_random_date(is_future=True)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_20_player_payout_with_casino_payout_invalid_game_type(self):
        payout = create_payout(payout_type="casino")
        payout.Game["GameType"] = "invalid"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="casino")
        self.assert_created(player)

    def test_tc_21_player_payout_with_casino_payout_invalid_game_identifier(self):
        payout = create_payout(payout_type="casino")
        payout.Game["GameIdentifier"] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="casino")
        self.assert_not_created(request_id)

    def test_tc_22_player_payout_with_sport_payout_past_game_date(self):
        payout = create_payout(payout_type="sport")
        payout.EventDate = generate_random_date(is_future=False)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="sport")
        self.assert_created(player)

    def test_tc_23_player_payout_with_sport_payout_invalid_event_date(self):
        payout = create_payout(payout_type="sport")
        payout.Game['EventDate'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="sport")
        self.assert_created(player)

    def test_tc_24_player_payout_with_sport_payout_live_not_boolean(self):
        payout = create_payout(payout_type="sport")
        payout.Game['Live'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="sport")
        self.assert_not_created(request_id)

    def test_tc_25_player_payout_with_sport_payout_sport_invalid(self):
        payout = create_payout(payout_type="sport")
        payout.Game['Sport'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="sport")
        self.assert_not_created(request_id)

    def test_tc_26_player_payout_with_sport_payout_sport_null(self):
        payout = create_payout(payout_type="sport")
        payout.Game['League'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="sport")
        self.assert_not_created(request_id)

    def test_tc_27_player_payout_with_bet_payout_past_event_date(self):
        payout = create_payout(payout_type="bet")
        payout.GameEventDate = generate_random_date(is_future=False)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    def test_tc_28_player_payout_with_bet_payout_null_event(self):
        payout = create_payout(payout_type="bet")
        payout.Event = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    def test_tc_29_player_payout_with_bet_payout_null_event_category(self):
        payout = create_payout(payout_type="bet")
        payout.Game['EventCategory'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    def test_tc_30_player_payout_with_lottery_payout_past_event_date(self):
        payout = create_payout(payout_type="lottery")
        payout.DrawDate = generate_random_date(is_future=False)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_created(player)

    def test_tc_31_player_payout_with_lottery_payout_invalid_event(self):
        payout = create_payout(payout_type="lottery")
        payout.Game['Name'] = "invalid"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_created(player)

    def test_tc_32_player_payout_with_lottery_payout_invalid_event_category(self):
        payout = create_payout(payout_type="bet")
        payout.Game['Category']= None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    def test_tc_33_player_payout_with_esport_payout_empty_game(self):
        payout = create_payout(payout_type="esport")
        payout.Game = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_not_created(request_id)

    def test_tc_34_player_payout_with_esport_payout_empty_league(self):
        payout = create_payout(payout_type="esport")
        payout.League = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_35_player_payout_with_esport_payout_empty_event(self):
        payout = create_payout(payout_type="esport")
        payout.Event = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_36_player_payout_with_esport_payout_empty_category(self):
        payout = create_payout(payout_type="esport")
        payout.Category = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_37_player_payout_with_esport_payout_past_event_date(self):
        payout = create_payout(payout_type="esport")
        payout.EventDate = generate_random_date(is_future=False)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_38_player_payout_with_esport_payout_null_game(self):
        payout = create_payout(payout_type="esport")
        payout.Game = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_not_created(request_id)

    def test_tc_39_player_payout_with_esport_payout_null_league(self):
        payout = create_payout(payout_type="esport")
        payout.Game['League'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_not_created(request_id)

    def test_tc_40_player_payout_with_esport_payout_null_event(self):
        payout = create_payout(payout_type="esport")
        payout.Game['Event'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_not_created(request_id)

    def test_tc_41_player_payout_with_esport_payout_null_category(self):
        payout = create_payout(payout_type="esport")
        payout.Game['EventCategory'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_42_player_payout_with_esport_payout_null_event_date(self):
        payout = create_payout(payout_type="esport")
        payout.Game['EventDate'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_created(player)

    def test_tc_43_player_payout_with_esport_payout_string_event_date(self):
        payout = create_payout(payout_type="esport")
        payout.Game['EventDate'] = "test_date"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="esport")
        self.assert_not_created(request_id)

    def test_tc_44_player_payout_with_parimutuel_payout_string_event_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['EventDate'] = "test_date"
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_45_player_payout_with_parimutuel_payout_null_event_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['EventDate'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_created(player)

    def test_tc_46_player_payout_with_parimutuel_payout_empty_event_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['EventDate'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_47_player_payout_with_parimutuel_payout_past_event_date(self):
        payout = create_payout(payout_type="parimutuel")
        payout.EventDate = generate_random_date(is_future=False)
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_created(player)

    def test_tc_48_player_payout_with_parimutuel_payout_emty_event(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['Event'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_49_player_payout_with_parimutuel_payout_null_event(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['Event'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_50_player_payout_with_parimutuel_payout_null_breed(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['Breed'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_51_player_payout_with_parimutuel_payout_empty_breed(self):
        payout = create_payout(payout_type="parimutuel")
        payout.Game['Breed'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="parimutuel")
        self.assert_not_created(request_id)

    def test_tc_52_player_payout_with_lottery_payout_null_event_date(self):
        payout = create_payout(payout_type="lottery")
        payout.Game['DrawDate'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_created(player)

    def test_tc_52_player_payout_with_lottery_payout_empty_event_date(self):
        payout = create_payout(payout_type="lottery")
        payout.Game['DrawDate'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_not_created(request_id)

    def test_tc_53_player_payout_with_lottery_payout_empty_event(self):
        payout = create_payout(payout_type="lottery")
        payout.Game['Name'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_not_created(request_id)

    def test_tc_54_player_payout_with_lottery_payout_null_event(self):
        payout = create_payout(payout_type="lottery")
        payout.Game['Name'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="lottery")
        self.assert_not_created(request_id)

    def test_tc_55_player_payout_with_lottery_payout_empty_event_category(self):
        payout = create_payout(payout_type="bet")
        payout.Game['Category'] = ""
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    def test_tc_56_player_payout_with_lottery_payout_null_event_category(self):
        payout = create_payout(payout_type="bet")
        payout.Game['Category'] = None
        player, payout, request_id = self._create_player_with_payout(payouts=[payout],
                                                                     payout_type="bet")
        self.assert_created(player)

    @staticmethod
    def get_payout_from_db(player):
        url = "http://{}/payouts?customer_id={}".format(get_config().get("test_framework", "db"), player.PlayerID)
        return get_until_not_empty(url, timeout=240)

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
    def _create_payouts(player, payout_type, payouts=[]):
        _payouts = [create_payout(payout_type=payout_type)] if payouts == [] else payouts
        logging.info("Creating payouts: {}".format([r.__dict__ for r in _payouts]))

        data = {"PlayerID": player.PlayerID, "InitID": int(generate_random_int()),
                "Payouts": [r.__dict__ for r in _payouts]}
        logging.info("Request data: {}".format(json.dumps(data)))
        response = requests.post(get_payout_resource(),
                                 data=json.dumps(data),
                                 headers=get_api_headers())

        logging.info("API response: {}".format(response.json()))
        return payouts, response.json()["RequestID"]

    def _create_player_with_payout(self, payout_type, payouts=[]):
        player = self._create_player()
        payouts, request_id = self._create_payouts(player, payout_type, payouts)
        return player, payouts, request_id

    def get_task(self, task_id):
        url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
        return get_until_attempt_greater_than_zero(url, timeout=100)

    def assert_created(self, player):
        result = self.get_payout_from_db(player)
        logging.info("DB result: {}".format(result))
        self.assertFalse(result == [])

    def assert_not_created(self, request_id):
        task = self.get_task(request_id)[0]
        logging.info("Task: {}".format(task))
        self.assertFalse(task["Error"] == "")
