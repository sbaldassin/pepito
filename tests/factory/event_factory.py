from tests.models.event import Event
from tests.utils.generator import generate_random_string, generate_random_date


def create_parimutuel_event(is_future=None):
    parimutuel_event = Event(
        event=generate_random_string(length=40),
        breed=generate_random_string(length=40),
        event_date=generate_random_date(include_time=True, is_future=is_future),
        event_id=generate_random_string(length=40)
    )
    return parimutuel_event

