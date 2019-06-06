from tests.models.game import Game
from tests.models.payout import Casino
from tests.utils.generator import generate_random_int, generate_random_date


def create_casino():
    payout = Casino(
        amount=float(generate_random_int(3)),
        product_id=int(generate_random_int(2)),
        currency="EUR",
        transaction_date=generate_random_date(include_time=True),
        game=Game().__dict__,
        count=4)
    return payout