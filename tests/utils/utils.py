from tests.config.config import get_config


def get_player_sign_up_resource(channel=1):
    return '{host}/player/signup/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_player_sign_in_resource(player_id, channel=1):
    return '{host}/player/{player}/signin/{channel}'.format(host=get_config().get("api", "host"),
                                                            channel=channel, player=player_id)


def get_player_flush_resource(player_id):
    return '{host}/player/flush/{player}'.format(host=get_config().get("api", "host"), player=player_id)


def get_player_update_resource():
    return '{host}/player/update'.format(host=get_config().get("api", "host"))


def get_withdrawal_resource():
    return '{host}/player/withdrawal/'.format(host=get_config().get("api", "host"))


def get_deposit_resource():
    return '{host}/player/deposit/1'.format(host=get_config().get("api", "host"))


def get_wagers_parimutuel_resource(channel=1):
    return '{host}/wagers/parimutuel/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_api_headers():
    headers = {
        'Authorization': 'Bearer {token}'.format(token=get_config().get("api", "authorization_header")),
        'Content-Type': 'application/json'
    }

    return headers


def get_api_ok_message():
    return 'OK'
