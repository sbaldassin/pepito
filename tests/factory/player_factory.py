from tests.models.player import Player
from tests.utils.generator import generate_random_int, generate_random_string, generate_random_phone_number, \
    generate_random_date, generate_random_country_code, generate_random_language_code


def create_random_player(player_id_length=5):
    player = Player(player_id=generate_random_int(length=player_id_length),
                    name=generate_random_string(),
                    email="{}@test.com".format(generate_random_string()),
                    surname=generate_random_string(),
                    country_code=generate_random_country_code(),
                    city=generate_random_string(),
                    zip_code=generate_random_int(),
                    state=generate_random_string(),
                    mobile_phone=generate_random_phone_number(),
                    signup_date=generate_random_date(),
                    date_of_bith=generate_random_date(),
                    custom_int_1=0,
                    custom_int_2=0,
                    custom_int_3=0,
                    custom_int_4=0,
                    custom_string=0,
                    custom_string_2=0,
                    custom_string_3=0,
                    custom_string_4=0,
                    time_zone="UTC-4",
                    language_code=generate_random_language_code(),
                    btag="",
                    promo_code="",
                    tracking_code="",
                    optout_email=True,
                    optout_sms=True,
                    optout_push=True,
                    optout_mobile_push=True
                    )
    return player
