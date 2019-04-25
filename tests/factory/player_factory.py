from tests.models.player import Player
from tests.utils.generator import generate_random_int, generate_random_string, generate_random_state, \
    generate_random_date, generate_random_country_code, generate_random_language_code, generate_random_boolean


def create_random_player(player_id_length=5):
    player = Player(player_id=generate_random_int(length=player_id_length),
                    name=generate_random_string(),
                    email="{}@test.com".format(generate_random_string()),
                    surname=generate_random_string(),
                    country_code=generate_random_country_code(),
                    city=generate_random_string(),
                    zip_code=generate_random_int(),
                    state=generate_random_state(),
                    mobile_phone=generate_random_int(14),
                    signup_date=generate_random_date(include_time=True),
                    date_of_bith=generate_random_date(),
                    custom_int_1=generate_random_int(1),
                    custom_int_2=generate_random_int(2),
                    custom_int_3=generate_random_int(1),
                    custom_int_4=generate_random_int(2),
                    custom_string=generate_random_string(),
                    custom_string_2=generate_random_string(),
                    custom_string_3=generate_random_string(),
                    custom_string_4=generate_random_string(),
                    time_zone=generate_random_int(2),
                    language_code=generate_random_language_code(),
                    btag=generate_random_string(),
                    promo_code=generate_random_string(),
                    tracking_code=generate_random_string(),
                    optout_email=generate_random_boolean(),
                    optout_sms=generate_random_boolean(),
                    optout_push=generate_random_boolean(),
                    optout_mobile_push=generate_random_boolean()
                    )
    return player
