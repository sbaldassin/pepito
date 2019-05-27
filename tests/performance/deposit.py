import json

from locust import HttpLocust, seq_task, TaskSequence

from tests.factory.player_factory import create_random_player
from tests.factory.revenue_factory import create_revenue
from tests.utils.generator import generate_random_int
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_deposit_resource


class DepositTestCase(TaskSequence):

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
        transactions = [create_revenue() for i in range(100)]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Transactions": [r.__dict__ for r in transactions]}
        self.client.post(get_deposit_resource(),
                         data=json.dumps(data),
                         headers=get_api_headers())


class Casino(HttpLocust):
    task_set = DepositTestCase
    min_wait = 5000
    max_wait = 9000