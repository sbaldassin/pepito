

class GameSession:

    def __init__(self, game_type, game_identifier, session_date):
        self.GameType = game_type
        self.GameIdentifier = game_identifier
        self.SessionDate = session_date


class GameSessionRequest:

    def __init__(self, player_id, init_id):
        self.PlayerID = player_id
        self.InitID = init_id
        self.GameSessions = []

    def add_game_session(self, game_session):
        self.GameSessions.append(game_session)