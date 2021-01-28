import shutil

import lucene
from lupyne import engine

from org.apache.lucene.analysis.core import WhitespaceTokenizer

from Core.Data import Data




class InvertedIndex:


    lucene.initVM()


    def __init__(self, index_name):

        self.__indexer = engine.Indexer(directory=Data.get(index_name), analyzer=InvertedIndex.__analyzer())

        self.__indexer.set('terms', engine.Field.Text, stored=False, tokenized=True)  # index_options=DOCS_AND_FREQS_AND_POSITIONS
        self.__indexer.set('text', engine.Field.Text, stored=True, tokenized=False, indexOptions=None)


    @staticmethod
    def delete(index_name):
        shutil.rmtree(Data.get(index_name))



    def add(self, text, terms=None):

        self.__indexer.add(terms=terms, text=text)

        self.__indexer.commit()


    def add_multiple(self, items):

        for item in items:
            self.__indexer.add(terms=item[1], text=item[0])

        self.__indexer.commit()


    def search(self, terms, limit_results=10):

        term_queries = [engine.Query.term('terms', term) for term in terms]
        query = engine.Query.any(*term_queries)

        return self.__indexer.search(query)[:limit_results]


    def terms(self, counts=True):

        for term in self.__indexer.terms(name='terms', counts=counts):
            yield term


    def docs(self, term, counts=True):

        for doc in self.__indexer.docs(name='terms', value=term, counts=counts):
            yield doc



    @staticmethod
    def __analyzer():
        return engine.Analyzer(WhitespaceTokenizer)





