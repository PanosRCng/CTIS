import shutil

import lucene
from lupyne import engine

from Core.Data import Data



lucene.initVM()




class ContextsCache:


    def __init__(self, index_name):

        self.__indexer = engine.Indexer(directory=Data.get(index_name))

        self.__indexer.set('title', engine.Field.Text, stored=False, tokenized=False)
        self.__indexer.set('context', engine.Field.Text, stored=True, tokenized=False, indexOptions=None)


    @staticmethod
    def delete(index_name):
        shutil.rmtree(Data.get(index_name))



    def set(self, title, context):

        self.__indexer.add(title=title, context=context)

        self.__indexer.commit()


    def get(self, title):

        results = self.__indexer.search( engine.Query.term('title', title) )

        if len(results) == 0:
            return None

        return results[0]['context']


