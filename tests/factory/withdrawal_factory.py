from tests.models.withdrawal import Withdrawal
from tests.utils.generator import generate_random_int, generate_random_date


def create_withdrawal():
    withdrawal = Withdrawal(
        amount=generate_random_int(3),
        currency="USD",
        transaction_date=generate_random_date())

    return withdrawal
