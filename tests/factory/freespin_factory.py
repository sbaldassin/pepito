from tests.factory.player_factory import create_random_player
from tests.models.facts import FreeSpinFact
from tests.models.freespin import Freespin
from tests.utils.generator import generate_random_int, generate_random_string, generate_random_date


def create_freespin(is_future=False):
    freespin = Freespin(
        value=generate_random_int(),
        transaction_date=generate_random_date(include_time=True, is_future=is_future),
        identifier=generate_random_string(100))
    return freespin


def create_freespin_fact():
    player = create_random_player()
    bonus = create_freespin()
    return FreeSpinFact(player, bonus)
