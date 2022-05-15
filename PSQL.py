import os
from config import PSQL_USER, PSQL_PASSWORD, PSQL_HOST, PSQL_PORT, PSQL_DATABASE

import psycopg2
from psycopg2 import Error



class PSQL:
    def __init__(self, user=os.getenv("PSQL_USER"),
                 password=os.getenv("PSQL_PASSWORD"),
                 host=os.getenv("PSQL_HOST"),
                 port=os.getenv("PSQL_PORT"),
                 database=os.getenv("PSQL_DATABASE")):
        try:
            connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

            self.cursor = connection.cursor()
            self.cursor.execute("SELECT * FROM table_doc")
            print(self.cursor.fetchall())
        except (Exception, Error) as error:
            print("Error while working with PostgreSQL", error)

        finally:
            if connection:
                connection.closed