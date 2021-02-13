from Core.CTIS.QueryCache.QueryCache import QueryCache
from Core.Config import Config
from Core.ElasticSearch.ES import ES
from Core.ElasticSearch.ESService import ESService
from Core.Logger import Logger




class ElasticSearchQueryCache(QueryCache):


    def __init__(self, cache_name):

        self.__cache_name = cache_name

        if ES.connection('es') is None:
            Logger.log(__name__, 'could not connect to elasticsearch', type='error')
            return

        ESService.create_index(self.__cache_name, Config.get('elasticsearch')['indices_settings'][self.__cache_name])



    def set(self, query, response):
        ES.connection('es').index(index=self.__cache_name, id=query, body={"response": response})


    def get(self, query):

        res = ESService.get_by_id(self.__cache_name, query)

        if res is None:
            return None

        return res['_source']['response']





