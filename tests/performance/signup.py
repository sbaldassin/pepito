import json

from locust import HttpLocust, TaskSet, task

from tests.factory.player_factory import create_random_player
from tests.utils.utils import get_player_sign_up_resource, get_api_headers


class SignUp(TaskSet):

    @task
    def sign_up(self):
        player = create_random_player(player_id_length=30)
        self.client.post(get_player_sign_up_resource(channel=1),
                         data=json.dumps(player.__dict__),
                         headers=get_api_headers())

class UserSignUp(HttpLocust):
    task_set = SignUp
    min_wait = 5000
    max_wait = 9000
