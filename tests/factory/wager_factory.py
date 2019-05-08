from tests.models.wager import ParimutuelWager, WagerCasino, WagerSport, WagerBet, WagerEsport, WagerLottery
from tests.utils.generator import generate_random_int, generate_random_date, generate_random_currency, \
    generate_random_string


def create_wager_casino():
    wager = WagerCasino(
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


def create_wager_sport():
    wager = WagerSport(
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


def create_wager_bet():
    wager = WagerBet(
        event_category = "Weather",
        event_date = generate_random_date(),
        event = "Rainy",
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager


def create_wager_esport():
    wager = WagerEsport(
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


def create_wager_lottery():
    wager = WagerLottery(
        name = "Euro millions",
        category = "EU based lottery",
        draw_date = generate_random_date(),
        currency = "EUR",
        value = generate_random_int(),
        transaction_date = generate_random_date(),
        count = 1
    )
    return wager
