
import pyodbc

from tests.config.config import get_config
from tests.db.queries import SELECT_PLAYER


class MsSqlDriver:

    def __init__(self):
        server = get_config().get("mssql", "server")
        database = get_config().get("mssql", "database_name")
        username = get_config().get("mssql", "username")
        password = get_config().get("mssql", "password")
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

    def get_player(self, player):
        cursor = self.connection.cursor()
        cursor.execute(SELECT_PLAYER.replace("ADD_PLAYER_ID", player.PlayerID))
        return cursor.fetchone()
