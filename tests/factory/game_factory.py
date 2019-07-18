from tests.models.game import CasinoGame
from tests.utils.generator import generate_random_int, generate_random_string, generate_random_state, \
    generate_random_date, generate_random_country_code, generate_random_language_code, generate_random_boolean, generate_random_productid


def create_random_game():
    length = 20
    game = CasinoGame(game_type=generate_random_string(length), game_identifier=generate_random_string(length))
    return game
