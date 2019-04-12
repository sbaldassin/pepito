
import pyodbc

from tests.config.config import get_config
from tests.db.queries import SELECT_PLAYER_FROM_Q_NET_CUSTOMER, SELECT_PLAYER_FROM_Q_NET_DW_FACT_SIGNUP


class MsSqlDriver:

    def __init__(self):
        server = get_config().get("mssql", "server")
        database = get_config().get("mssql", "database_name")
        username = get_config().get("mssql", "username")
        password = get_config().get("mssql", "password")
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

    def get_player_from_customer(self, player):
        cursor = self.connection.cursor()
        cursor.execute(SELECT_PLAYER_FROM_Q_NET_CUSTOMER.replace("ADD_PLAYER_ID", player.PlayerID))
        return cursor.fetchone()

    def get_player_from_fact_signup(self, player):
        cursor = self.connection.cursor()
        cursor.execute(SELECT_PLAYER_FROM_Q_NET_DW_FACT_SIGNUP.replace("ADD_PLAYER_ID", player.PlayerID))
        return cursor.fetchone()
