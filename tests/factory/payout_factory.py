from random import randint

from tests.models.game import CasinoGame, SportGame, BetGame, EsportGame, LotteryGame, ParimutuelGame
from tests.models.payout import Payout
from tests.utils.generator import generate_random_int, generate_random_date


def create_payout(payout_type, **kwargs):
    payout = Payout(
        amount=float(generate_random_int(3)),
        product_id=game_ids[payout_type],
        currency="EUR",
        transaction_date=generate_random_date(include_time=True),
        game=game_types[payout_type]().__dict__,
        count=4)
    return payout


game_types = {
    "casino": CasinoGame,
    "sport": SportGame,
    "bet": BetGame,
    "esport": EsportGame,
    "lottery": LotteryGame,
    "parimutuel": ParimutuelGame
}


game_ids = {
    "casino": 1,
    "sport": 2,
    "bet": 3,
    "esport": 4,
    "lottery": 5,
    "parimutuel": 6
}
