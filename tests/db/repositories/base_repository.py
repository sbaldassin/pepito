import urllib

from sqlalchemy_dao import Dao

from tests.config.config import get_config


class BaseRepository(object):
    def __init__(self):
        server = get_config().get("mssql", "server")
        username = get_config().get("mssql", "username")
        password = get_config().get("mssql", "password")
        database = get_config().get("mssql", "database_name")
        params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.dao = Dao("mssql+pyodbc:///?odbc_connect=%s" % params)
        self.model = None
