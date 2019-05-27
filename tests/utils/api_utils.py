import json

import requests

from tests.config.config import get_config
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_api_headers, get_api_ok_message


# ARETO APIs method
def create_areto_api_object(self, resource, data):
    response = requests.post(resource, data=json.dumps(data), headers=get_api_headers())
    self.assertTrue(response.status_code, 200)
    body = response.json()
    assert body.get('Success'), True
    assert body.get('Message'), get_api_ok_message()
    request_id = body.get('RequestID')
    assert request_id == True
    return request_id


# INTERNAL API ENDPOINTS
def get_freespin_response(player_id):
    url = "http://{}/freespin?customer_id={}".format(get_config().get("test_framework", "db"), player_id)
    return get_until_not_empty(url, timeout=100)


def get_task(task_id):
    url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
    return get_until_not_empty(url, timeout=100)
