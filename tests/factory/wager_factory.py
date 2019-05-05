from tests.models.wager import Wager
from tests.utils.generator import generate_random_int, generate_random_date


def create_wager():
    wager = Wager(
        value=generate_random_int(),
        currency="EUR",
        transaction_date=generate_random_date(),
        game_type="Video slot",
        game_identifier=generate_random_int(),
        count=4)
    return wager
