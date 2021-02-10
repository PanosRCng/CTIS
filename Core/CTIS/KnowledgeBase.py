import json

from Core.Config import Config
from Core.CTIS.SearchEngine import SearchEngine
from Core.CTIS.QueryCache.QueryCache import QueryCache
from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.SQLiteDict import SQLiteDict



class KnowledgeBase:


    def __init__(self):

        self.__on_miss_backoff = Config.get('CTI')['knowledge_base']['on_miss_backoff']

        self.__search_engine = SearchEngine()
        self.__query_cache = QueryCache.create(Config.get('query_cache'))
        self.__contexts_cache = ContextsCache.create(Config.get('contexts_cache'))



    def featured_context_set(self, term):
        return [context for context in self.__get_contexts(self.__get_contexts_titles(term)) if context != '']



    def __get_contexts_titles(self, term):

        response = self.__query_cache.get(term)

        if response is not None:
            return json.loads(response)

        response = self.__search_engine.contexts_titles(term)
        self.__query_cache.set(term, response)

        return json.loads(response)


    def __get_contexts(self, titles):

        contexts = []
        misses = []

        for title, context in self.__contexts_cache.get(titles).items():

            if context is not None:
                contexts.append(context)
            else:
                misses.append(title)

        if self.__on_miss_backoff is True:
            for title in misses:
                SQLiteDict.storage(Config.get('backed_off_search')['store'])[title] = title

        else:

            new_contexts = self.__search_engine.contexts(misses)

            contexts += list(new_contexts.values())

            self.__contexts_cache.set_many(new_contexts)

        return contexts




