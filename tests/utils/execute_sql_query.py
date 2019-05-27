import argparse

import pyodbc

from tests.config.config import get_config


if __name__ == "__main__":
    # eg:
    # root@75c454b03053:/source_tests/tests/utils# python3 execute_sql_query.py "select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='Merchant';"

    parser = argparse.ArgumentParser(description='Script to execute sql queries.')
    parser.add_argument('sql', help='the query to be executed.')
    #parser.add_argument('env', help='Environment to connect to.', default="QA")
    args = parser.parse_args()

    # server = get_config().get("mssql", "server")
    # database = get_config().get("mssql", "database_name")
    # username = get_config().get("mssql", "username")
    # password = get_config().get("mssql", "password")
    server = 'tcp:aretostagingserver.database.windows.net'
    database = 'ARETOQA'
    username = 'VJazbani'
    password = 'STJt9n^h:RG(d<:T'

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute(args.sql)

    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()
