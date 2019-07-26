from tests.factory.player_factory import create_random_player
from tests.models.revenue import Revenue, RevenueFact
from tests.utils.generator import generate_random_int, generate_random_date


def create_revenue():
    revenue = Revenue(
        amount=generate_random_int(),
        currency="EUR",
        transaction_date=generate_random_date(),
        success=True,
        payment_method="Skrill")
    return revenue


def create_revenue_fact():
    return RevenueFact(create_random_player(), create_revenue())
