from sqlitedict import SqliteDict

from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.Data import Data



class SqliteDictContextsCache(ContextsCache):


    def __init__(self, cache_name):

        self.__cache_name = cache_name
        self.__cache = None



    def set(self, title, context):
        self.__get_cache()[title] = context


    def get(self, title):
        return self.__get_cache().get(title, default=None)



    def __get_cache(self):

        if self.__cache is None:
            self.__cache = SqliteDict(Data.get(self.__cache_name), autocommit=True)

        return self.__cache


