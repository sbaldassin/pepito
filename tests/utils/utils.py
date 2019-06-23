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


def get_deposit_resource(channel=1):
    return '{host}/player/deposit/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_bonus_resource():
    return '{host}/player/bonus'.format(host=get_config().get("api", "host"))


def get_freespin_resource():
    return '{host}/player/freespin'.format(host=get_config().get("api", "host"))


def get_wager_casino_resource(channel=1):
    return '{host}/player/wager/casino/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_payout_resource():
    return '{host}/player/payout/'.format(host=get_config().get("api", "host"))


def get_wager_esport_resource(channel=1):
    return '{host}/player/wager/esports/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_wager_lottery_resource(channel=1):
    return '{host}/player/wager/lottery/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_wager_sport_resource(channel=1):
    return '{host}/player/wager/sports/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_wager_betting_resource(channel=1):
    return '{host}/player/wager/betting/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_wagers_parimutuel_resource(channel=1):
    return '{host}/player/wager/parimutuel/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_game_session_resource(channel=1):
    return '{host}/player/game/{channel}'.format(host=get_config().get("api", "host"), channel=channel)


def get_dim_parimutuel_resource():
    return '{host}/dim/parimutuel'.format(host=get_config().get("api", "host"))


def get_dim_lottery_resource():
    return '{host}/dim/lottery'.format(host=get_config().get("api", "host"))


def get_dim_sports_resource():
    return '{host}/dim/sports'.format(host=get_config().get("api", "host"))


def get_api_headers():
    headers = {
        'Authorization': 'Bearer {token}'.format(token=get_config().get("api", "authorization_header")),
        'Content-Type': 'application/json'
    }

    return headers


def get_api_ok_message():
    return 'OK'

# API ERROR messages


def get_api_error_player_id_not_passed():
    return 'PlayerID not being passed'


def get_api_error_wager_list_empty():
    return 'Wager list is empty'


def get_api_error_event_list_empty():
    return 'No Data being passed'


# API Tasks error messages
def get_task_error_invalid_event():
    return 'Invalid event name on record number 1. No data saved.'


def get_task_error_invalid_lottery_event():
    return 'Invalid Name on record number 1. No data saved.'


def get_task_error_invalid_parimutuel_event():
    return 'Invalid Event on record number 1. No data saved.'


def get_task_error_invalid_sport_event():
    return 'Invalid Sport on record number 1. No data saved.'


def get_task_error_invalid_sport_league():
    return 'Invalid League on record number 1. No data saved.'


def get_task_error_invalid_event_name():
    return 'Invalid event name on record number 1. Couldn\'t proceed with wager cancellation.'


def get_task_error_invalid_breed():
    return 'Invalid breed on record number 1. No data saved.'


def get_task_error_invalid_breed_cancellation():
    return 'Invalid breed on record number 1.  Couldn\'t proceed with wager cancellation.'


def get_task_error_invalid_wager_value():
    return 'Invalid wager value on record number 1. No data saved.'


def get_task_error_invalid_value_cancellation():
    return 'Invalid wager value on record number 1.  Couldn\'t proceed with wager cancellation.'


def get_task_error_sql_overflow():
    return 'SqlDateTime overflow. Must be between 1/1/1753 12:00:00 AM and 12/31/9999 11:59:59 PM.'


def get_task_error_invalid_currency():
    return 'Invalid currency code on record number 1. No data saved.'


def get_task_error_invalid_currency_cancellation():
    return 'Invalid currency code on record number 1.  Couldn\'t proceed with wager cancellation.'


def get_task_error_invalid_identifier():
    return 'Identifier cannot be left empty on record number 1. No data saved.'


def get_task_error_invalid_value():
    return 'Invalid freespin value on record number 1. No data saved.'


def get_task_error_invalid_game_type():
    return 'Invalid game type on record number 1. No data saved.'


def get_task_error_invalid_game_identifier():
    return 'Invalid game identifier on record number 1. No data saved.'


def get_task_error_invalid_sport_identifier():
    return 'Invalid Sport identifier on record number 1. No data saved.'


def get_task_error_invalid_league_identifier():
    return 'Invalid League/tournament identifier on record number 1. No data saved.'


def get_task_error_invalid_event2():
    return 'Invalid Event on record number 1. Event is empty. No data saved.'


def get_task_error_wager_not_found():
    return 'Wager not found. Couldn\'t proceed with wager cancellation.'


def get_task_error_invalid_category():
    return 'Invalid Category on record number 1. No data saved'
