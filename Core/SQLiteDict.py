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
    def storage(storage_name):
        return SQLiteDict.__get_instance().__get_storage(storage_name)



    def __setup(self):
        self.__sqldicts = {}


    def __get_storage(self, storage_name):

        if self.__storage_exists(storage_name):
            return self.__sqldicts[storage_name]

        storage = SqliteDict(Data.get(storage_name), autocommit=True)

        if storage is None:
            return None

        self.__sqldicts[storage_name] = storage

        return self.__sqldicts[storage_name]


    def __storage_exists(self, storage_name):

        if storage_name not in self.__sqldicts:
            return False

        if self.__sqldicts[storage_name] is None:
            return False

        return True



