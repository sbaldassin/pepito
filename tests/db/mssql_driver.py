import pymssql

from tests.config.config import get_config
from tests.db.queries import SELECT_PLAYER


class MsSqlDriver:

    def __init__(self):
        self.connection = pymssql.connect(
            server=get_config().get("mssql", "server"),
            user=get_config().get("mssql", "username"),
            password=get_config().get("mssql", "password"),
            database=get_config().get("mssql", "database_name"))

    def get_player(self, player):
        cursor = self.connection.cursor()
        cursor.execute(SELECT_PLAYER.replace("ADD_PLAYER_ID", player.player_id))
        return cursor.fetchone()
