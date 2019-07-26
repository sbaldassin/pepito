from tests.factory.player_factory import create_random_player
from tests.models.withdrawal import Withdrawal, WithdrawalFact
from tests.utils.generator import generate_random_int, generate_random_date


def create_withdrawal():
    withdrawal = Withdrawal(
        amount=generate_random_int(3),
        currency="USD",
        transaction_date=generate_random_date())

    return withdrawal


def create_withdrawal_fact():
    return WithdrawalFact(create_random_player(), create_withdrawal())
