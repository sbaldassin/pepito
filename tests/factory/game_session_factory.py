from tests.models.game_session import GameSession, GameSessionRequest
from tests.utils.generator import generate_random_date, generate_random_string


def create_game_session():
    session = GameSession(
        session_date=generate_random_date(),
        game_type=generate_random_string(250),
        game_identifier=generate_random_string(100))
    return session


def create_game_session_request(player_id, init_id=None, total_sessions=1):
    if not player_id:
        player_id = generate_random_string(40),

    if not init_id:
        init_id = generate_random_string(40),

    session_request = GameSessionRequest(player_id, init_id)

    for i in range(total_sessions):
        session = GameSession(
            session_date=generate_random_date(is_future=True),
            game_type=generate_random_string(250),
            game_identifier=generate_random_string(100))
        session_request.add_game_session(session)
    return session_request
