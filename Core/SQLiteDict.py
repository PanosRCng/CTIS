from sqlitedict import SqliteDict
from Core.Data import Data


class SQLiteDict:

    __instance = None


    def __init__(self):

        if SQLiteDict.__instance is not None:
            return

        SQLiteDict.__instance = self
        self.__setup()



    @staticmethod
    def __get_instance():

        if SQLiteDict.__instance is None:
            SQLiteDict()

        return SQLiteDict.__instance


    @staticmethod
    def store(store_name):
        return SQLiteDict.__get_instance().__get_store(store_name)



    def __setup(self):
        self.__sqldicts = {}


    def __get_store(self, store_name):

        if self.__store_exists(store_name):
            return self.__sqldicts[store_name]

        store = SqliteDict(Data.get(store_name), autocommit=True)

        if store is None:
            return None

        self.__sqldicts[store_name] = store

        return self.__sqldicts[store_name]


    def __store_exists(self, store_name):

        if store_name not in self.__sqldicts:
            return False

        if self.__sqldicts[store_name] is None:
            return False

        return True



