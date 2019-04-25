from tests.config.config import get_config


def get_player_sign_up_resource(channel=1):
    return '{host}/player/signup/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_player_update_resource():
    return '{host}/player/update'.format(host=get_config().get("api", "host"))


def get_withdrawal_resource():
    return '{host}/player/withdrawal/'.format(host=get_config().get("api", "host"))

    
def get_api_headers():
    headers = {
        'Authorization': 'Bearer {token}'.format(token=get_config().get("api", "authorization_header")),
        'Content-Type': 'application/json'
    }

    return headers


def get_api_ok_message():
    return 'OK'
