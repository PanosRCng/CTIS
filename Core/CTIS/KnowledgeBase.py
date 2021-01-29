import json
from Core.CTIS.SearchEngine import SearchEngine
#from Core.CTIS.QueryCache import QueryCache
#from Core.CTIS.ContextsCache import ContextsCache
import asyncio

import time



class KnowledgeBase:


    def __init__(self):

        self.__search_engine = SearchEngine()
        #self.__query_cache = QueryCache('query_cache')
        #self.__contexts_cache = ContextsCache('contexts_cache')


    def run(corofn, *args):
        loop = asyncio.new_event_loop()
        try:
            coro = self.__context(title)(*args)
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        finally:
            loop.close()


    def featured_context_set(self, term):

        contexts = []

        print(time.time(), 'start')

        loop = asyncio.get_event_loop()
        #results = loop.run_until_complete(asyncio.gather(*[self.__context(title) for title in self.__contexts_titles(term)]))

        executor = ThreadPoolExecutor(max_workers=3)

        futures = [loop.run_in_executor(executor, run, asyncio.sleep, 1, title) for title in self.__contexts_titles(term)]

        #tasks = [loop.run_in_executor(executor, self.__context(title)) for title in self.__contexts_titles(term)]]

        print(await asyncio.gather( * futures))


        '''
        for title in self.__contexts_titles(term):

            context = self.__context(title)

            if context is None:
                continue

            contexts.append(context)
        '''
        print(time.time(), results)

        return contexts



    def __contexts_titles(self, term):

        #response = self.__query_cache.get(term)
        response = None

        if response is not None:
            return json.loads(response)

        response = self.__search_engine.contexts_titles(term)

        contexts_titles = json.loads(response)

        if len(contexts_titles) == 0:
            return []

        #self.__query_cache.set(term, response)

        return contexts_titles


    async def __context(self, title):

        #context = self.__contexts_cache.get(title)
        context = None

        if context is not None:
            return context

        await asyncio.sleep(3)
        context = self.__search_engine.context(title)

        if context is None:
            return None

        #self.__contexts_cache.set(title, context)

        return context



