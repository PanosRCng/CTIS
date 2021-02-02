import json

from Core.Config import Config
from Core.CTIS.SearchEngine import SearchEngine
from Core.CTIS.QueryCache.QueryCache import QueryCache
from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.SQLiteDict import SQLiteDict



class KnowledgeBase:


    def __init__(self, on_miss_backoff=False):

        self.__on_miss_backoff = on_miss_backoff

        self.__search_engine = SearchEngine()
        self.__query_cache = QueryCache.create(Config.get('query_cache'))
        self.__contexts_cache = ContextsCache.create(Config.get('contexts_cache'))



    def featured_context_set(self, term):

        contexts = []

        for title in self.__contexts_titles(term):

            context = self.__context(title)

            if context is None:
                continue

            contexts.append(context)

        return contexts



    def __contexts_titles(self, term):

        response = self.__query_cache.get(term)

        if response is not None:
            return json.loads(response)

        response = self.__search_engine.contexts_titles(term)

        contexts_titles = json.loads(response)

        if len(contexts_titles) == 0:
            return []

        self.__query_cache.set(term, response)

        return contexts_titles


    def __context(self, title):

        context = self.__contexts_cache.get(title)

        if context is not None:
            return context

        if self.__on_miss_backoff is True:
            SQLiteDict.store(Config.get('backedoff_store'))[title] = title
            return None

        context = self.__search_engine.context(title)

        if context is None:
            return None

        self.__contexts_cache.set(title, context)

        return context



