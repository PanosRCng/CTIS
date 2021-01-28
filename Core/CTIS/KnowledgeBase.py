import json
from Core.CTIS.SearchEngine import SearchEngine
from Core.CTIS.QueryCache import QueryCache
from Core.CTIS.ContextsCache import ContextsCache




class KnowledgeBase:


    def __init__(self):

        self.__search_engine = SearchEngine()
        self.__query_cache = QueryCache('query_cache')
        self.__contexts_cache = ContextsCache('contexts_cache')



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

        context = self.__search_engine.context(title)

        if context is None:
            return None

        self.__contexts_cache.set(title, context)

        return context



