from tests.models.wager import Casino, Parimutuel, Sport, Bet, Esport, Lottery
from tests.utils.generator import generate_random_int, generate_random_date, generate_random_currency


def create_casino():
    wager = Casino(
        value=generate_random_int(),
        currency="EUR",
        transaction_date=generate_random_date(),
        game_type="Video slot",
        game_identifier=generate_random_int(),
        count=4)
    return wager


def create_parimutuel():
    wager = Parimutuel(
        value=generate_random_int(),
        currency=generate_random_currency(),
        transaction_date=generate_random_date(include_time=True),
        count=generate_random_int(length=1))
    return wager


def create_sport():
    wager = Sport(
        sport = "Football",
        league = "Serie A",
        event = "AC Milan vs Juventus FC",
        live = True,
        event_id = generate_random_int(),
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager


def create_bet():
    wager = Bet(
        event_category = "Weather",
        event_date = generate_random_date(),
        event = "Rainy",
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager


def create_esport():
    wager = Esport(
        game = "CS Zero",
        league = "League 1",
        event_id = generate_random_int(),
        event_category = "Day 2",
        event_date = generate_random_date(),
        event = "Mark Brown vs Matt White",
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager


def create_lottery():
    wager = Lottery(
        name = "Euro millions",
        category = "EU based lottery",
        draw_date = generate_random_date(),
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager
