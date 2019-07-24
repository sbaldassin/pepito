from tests.factory.game_session_factory import create_game_session
from tests.factory.player_factory import create_random_player
from tests.models.game import CasinoGame
from tests.models.game_session import GameSessionFact
from tests.utils.generator import generate_random_string


def create_random_game():
    length = 20
    game = CasinoGame(game_type=generate_random_string(length), game_identifier=generate_random_string(length))
    return game


def create_casino_game_fact():
    player = create_random_player()
    game_session = create_game_session()
    return GameSessionFact(player, game_session)
