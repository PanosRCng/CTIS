import shutil


from Core.Data import Data



class QueryCache:


    def __init__(self, cache_name):
        self.__cache = plyvel.DB(Data.get(cache_name), create_if_missing=True)


    @staticmethod
    def delete(cache_name):
        shutil.rmtree(Data.get(cache_name))



    def set(self, query, response):
        self.__cache.put(query.encode(), response.encode())


    def get(self, query):

        results = self.__cache.get(query.encode())

        if results is None:
            return None

        return results


