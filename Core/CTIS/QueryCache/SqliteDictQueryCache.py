from Core.CTIS.QueryCache.QueryCache import QueryCache
from Core.SQLiteDict import SQLiteDict



class SqliteDictQueryCache(QueryCache):


    def __init__(self, cache_name):
        self.__cache_name = cache_name



    def set(self, query, response):
        SQLiteDict.store(self.__cache_name)[query] = response


    def get(self, query):
        return SQLiteDict.store(self.__cache_name).get(query, default=None)





