import shutil

import lucene
from lupyne import engine

from Core.Data import Data



lucene.initVM()




class QueryCache:


    def __init__(self, index_name):

        self.__indexer = engine.Indexer(directory=Data.get(index_name))

        self.__indexer.set('query', engine.Field.Text, stored=False, tokenized=False)
        self.__indexer.set('response', engine.Field.Text, stored=True, tokenized=False, indexOptions=None)


    @staticmethod
    def delete(index_name):
        shutil.rmtree(Data.get(index_name))



    def set(self, query, response):

        self.__indexer.add(query=query, response=response)

        self.__indexer.commit()


    def get(self, query):

        results = self.__indexer.search( engine.Query.term('query', query) )

        if len(results) == 0:
            return None

        return results[0]['response']


