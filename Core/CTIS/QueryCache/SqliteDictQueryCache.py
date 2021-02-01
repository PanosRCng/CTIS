from sqlitedict import SqliteDict

from Core.CTIS.QueryCache.QueryCache import QueryCache
from Core.Data import Data



class SqliteDictQueryCache(QueryCache):


    def __init__(self, cache_name):

        self.__cache_name = cache_name
        self.__cache = None



    def set(self, query, response):
        self.__get_cache()[query] = response


    def get(self, query):
        return self.__get_cache().get(query, default=None)



    def __get_cache(self):

        if self.__cache is None:
            self.__cache = SqliteDict(Data.get(self.__cache_name), autocommit=True)

        return self.__cache


