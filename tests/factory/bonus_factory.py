from tests.models.bonus import Bonus
from tests.utils.generator import generate_random_int, generate_random_date, generate_random_productid


def create_bonus():
    bonus = Bonus(
        value=generate_random_int(),
        currency="EUR",
        transaction_date=generate_random_date(),
        identifier="Deposit bonus 50% max 2K x50 wagers",
        product_id=generate_random_productid())
    return bonus
