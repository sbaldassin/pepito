import json
from random import randint

from locust import HttpLocust, seq_task, TaskSequence, task

from tests.factory.bonus_factory import create_bonus
from tests.factory.payout_factory import create_payout
from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue
from tests.factory.wager_factory import create_lottery, create_esport, create_sport, create_casino, create_bet
from tests.factory.withdrawal_factory import create_withdrawal
from tests.utils.generator import generate_random_int
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_deposit_resource, \
    get_withdrawal_resource, get_bonus_resource, get_wager_betting_resource, get_wager_lottery_resource, \
    get_wager_esport_resource, get_wager_sport_resource, get_wager_casino_resource, get_payout_resource


class UsersTestCase(TaskSequence):

    player = None

    @seq_task(1)
    def sign_up(self):
        player = create_random_player(player_id_length=30)
        self.player = player
        self.client.post(get_player_sign_up_resource(channel=1),
                         data=json.dumps(player.__dict__),
                         headers=get_api_headers())

    @seq_task(2)
    def create_deposit(self):
        transactions = [create_revenue()]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Transactions": [r.__dict__ for r in transactions]}
        self.client.post(get_deposit_resource(),
                         data=json.dumps(data),
                         headers=get_api_headers())

    @seq_task(2)
    def create_five_wagers(self):
        wagers, url = self.create_random_wager()
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Wagers": [r.__dict__ for r in wagers]}
        self.client.post(url,
                         data=json.dumps(data),
                         headers=get_api_headers())

    @seq_task(2)
    def create_withdrawal(self):
        withdrawals = [create_withdrawal()]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Withdrawals": [r.__dict__ for r in withdrawals]}
        self.client.post(get_withdrawal_resource(),
                         data=json.dumps(data),
                         headers=get_api_headers())

    @seq_task(2)
    def create_bonus(self):
        bonuses = [create_bonus()]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Bonuses": [r.__dict__ for r in bonuses]}
        self.client.post(get_bonus_resource(),
                         data=json.dumps(data),
                         headers=get_api_headers())

    @seq_task(2)
    def create_payout(self):
        bonuses = [create_payout(self.get_payout_type())]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Payouts": [r.__dict__ for r in bonuses]}
        self.client.post(get_payout_resource(),
                         data=json.dumps(data),
                         headers=get_api_headers())

    def create_random_wager(self):
        wagers_list = [
            {"create_method": create_bet, "resource_url": get_wager_betting_resource(), "count": 5},
            {"create_method": create_casino, "resource_url": get_wager_casino_resource(), "count": 100},
            {"create_method": create_sport, "resource_url": get_wager_sport_resource(), "count": 5},
            {"create_method": create_esport, "resource_url": get_wager_esport_resource(), "count": 5},
            {"create_method": create_lottery, "resource_url": get_wager_lottery_resource(), "count": 5}
        ]

        index = randint(0, 4)
        return [wagers_list[index]["create_method"]() for i in range(wagers_list[index]["count"])], wagers_list[index]["resource_url"]

    def get_payout_type(self):
        payouts_list = ["bet", "casino", "sport", "esport", "lottery"]
        index = randint(0, 4)
        return payouts_list[index]


class UsersTestCase(HttpLocust):
    task_set = UsersTestCase
    min_wait = 1000
    max_wait = 2000
