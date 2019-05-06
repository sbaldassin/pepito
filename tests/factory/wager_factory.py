from tests.models.wager import ParimutuelWager, Wager
from tests.utils.generator import generate_random_int, generate_random_date, generate_random_currency


def create_wager():
    wager = Wager(
        value=generate_random_int(),
        currency="EUR",
        transaction_date=generate_random_date(),
        game_type="Video slot",
        game_identifier=generate_random_int(),
        count=4)
    return wager


def create_parimutuel_wager():
    wager = ParimutuelWager(
        value=generate_random_int(),
        currency=generate_random_currency(),
        transaction_date=generate_random_date(include_time=True),
        count=generate_random_int(length=1))
    return wager
