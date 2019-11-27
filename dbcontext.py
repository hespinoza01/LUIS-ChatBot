import sqlite3

class DbContext():
    def __init__(self, dbfile='dbfile.db'):
        self.dbfile = dbfile

    def __connect(self):
        try:
            self.__connection = sqlite3.connect(self.dbfile)
            self.__cursor = self.__connection.cursor()
        except sqlite3.Error as err:
            print(f"Error to DB connect: ${err}")

    def __close(self):
        self.__connection.close()

    def read(self, query_string, query_params=[]):
        result = None

        try:
            self.__connect()
            if len(query_params) > 0:
                self.__cursor.execute(query_string, query_params)
            else:
                self.__cursor.execute(query_string)

            result = self.__cursor.fetchall()
        except sqlite3.Error as err:
            print(f"Error on Database Read: ${err}")
        finally:
            self.__close()

        return result

    def execute(self, query_string):
        result = False

        try:
            self.__connect()
            self.__cursor.execute(query_string)

            result = True
        except sqlite3.Error as err:
            print(f"Error on Database Execute: ${err}")
        finally:
            self.__close()

        return result
