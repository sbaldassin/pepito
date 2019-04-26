from tests.models.revenue import Revenue
from tests.utils.generator import generate_random_int, generate_random_date


def create_revenue():
    revenue = Revenue(
        amount=generate_random_int(),
        currency="USD",
        transaction_date=generate_random_date(),
        success=True,
        payment_method="Skrill")
    return revenue