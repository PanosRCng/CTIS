from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.SQLiteDict import SQLiteDict



class SqliteDictContextsCache(ContextsCache):


    def __init__(self, cache_name):
        self.__cache_name = cache_name



    def set(self, title, context):
        SQLiteDict.store(self.__cache_name)[title] = context


    def set_many(self, contexts_dict):

        for title, context in contexts_dict.items():
            SQLiteDict.store(self.__cache_name)[title] = context


    def get(self, titles):

        contexts = {}

        for title in titles:
            contexts[title] = SQLiteDict.store(self.__cache_name).get(title, default=None)

        return contexts





