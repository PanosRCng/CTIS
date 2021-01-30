import shutil


from Core.Data import Data



class ContextsCache:


    def __init__(self, cache_name):
        self.__cache = plyvel.DB(Data.get(cache_name), create_if_missing=True)

        #self.__indexer.set('title', engine.Field.Text, stored=False, tokenized=False)
        #self.__indexer.set('context', engine.Field.Text, stored=True, tokenized=False, indexOptions=None)


    @staticmethod
    def delete(cache_name):
        shutil.rmtree(Data.get(cache_name))



    def set(self, title, context):
        self.__cache.put(title.encode(), context.encode())


    def get(self, title):

        results = self.__cache.get(title.encode())

        if results is None:
            return None

        return results


