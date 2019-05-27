import json

from locust import HttpLocust, TaskSet, seq_task, TaskSequence

from tests.factory.player_factory import create_random_player
from tests.factory.wager_factory import create_wager_casino
from tests.utils.generator import generate_random_int
from tests.utils.utils import get_player_sign_up_resource, get_api_headers, get_wager_casino_resource


class CasinoTestCase(TaskSequence):

    player = None

    @seq_task(1)
    def sign_up(self):
        player = create_random_player(player_id_length=30)
        self.player = player
        self.client.post(get_player_sign_up_resource(channel=1),
                         data=json.dumps(player.__dict__),
                         headers=get_api_headers())

    @seq_task(2)
    def create_wager_casino(self):
        wagers = [create_wager_casino() for i in range(100)]
        data = {"PlayerID": self.player.PlayerID, "InitID": generate_random_int(),
                "Wagers": [r.__dict__ for r in wagers]}
        self.client.post(get_wager_casino_resource(channel=1),
                         data=json.dumps(data),
                         headers=get_api_headers())



class Casino(HttpLocust):
    task_set = CasinoTestCase
    min_wait = 5000
    max_wait = 9000