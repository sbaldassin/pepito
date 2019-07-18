import json

import requests

from tests.config.config import get_config
from tests.utils.getters import get_until_not_empty
from tests.utils.utils import get_api_headers, get_api_ok_message
from tests.utils.retry import retry


# ARETO APIs method
def create_areto_api_object(resource, data, success=True, msg=get_api_ok_message()):
    response = requests.post(resource, data=json.dumps(data), headers=get_api_headers())
    assert response.status_code == 200
    body = response.json()
    assert body.get('Success') == success
    assert body.get('Message').lower() == msg.lower()
    request_id = body.get('RequestID')
    if success:
        assert request_id is not None
    else:
        assert request_id == 0
    return request_id


# INTERNAL API ENDPOINTS
def get_freespin_response(player_id):
    url = "http://{}/freespin?customer_id={}".format(get_config().get("test_framework", "db"), player_id)
    return get_until_not_empty(url, timeout=200)


def get_game_session_response(player_id):
    url = "http://{}/game?customer_id={}".format(get_config().get("test_framework", "db"), player_id)
    return get_until_not_empty(url, timeout=150)


def get_task(task_id):
    url = "http://{}/tasks?task_id={}".format(get_config().get("test_framework", "db"), task_id)
    return get_until_not_empty(url, timeout=100)


def get_dim_game(name):
    url = "http://{}/dim_game?name={}".format(get_config().get("test_framework", "db"), name)
    return get_until_not_empty(url, timeout=100)


@retry(AssertionError, tries=5, delay=5, backoff=2)
def verify_api_error(request_id, error):
    task = get_task(request_id)
    assert len(task) == 1
    assert task[0]['Error'].lower() == error.lower()
