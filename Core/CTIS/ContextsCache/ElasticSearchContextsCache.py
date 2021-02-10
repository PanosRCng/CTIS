from elasticsearch import helpers

from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.ES import ES
from Core.ESService import ESService
from Core.Logger import Logger
from Core.Config import Config




class ElasticSearchContextsCache(ContextsCache):


    def __init__(self, cache_name):

        self.__cache_name = cache_name

        if ES.connection('es') is None:
            Logger.log(__name__, 'could not connect to elasticsearch', type='error')
            return

        ESService.create_index(Config.get('contexts_cache')['name'])


    def set(self, title, context):
        ES.connection('es').index(index=self.__cache_name, id=title, body={"response": context})


    def set_many(self, contexts_dict):

        body = ({
            "_index": self.__cache_name,
            "_id": title,
            "context": context
        } for title, context in contexts_dict.items())

        helpers.bulk(ES.connection('es'), body, chunk_size=500, request_timeout=100)


    def get(self, titles):

        contexts = {}

        for title in titles:
            contexts[title] = None

        for hit in ESService.get_by_ids(self.__cache_name, titles):

            if 'context' not in hit['_source']:
                print(hit)

            contexts[hit['_id']] = hit['_source']['context']

        return contexts



