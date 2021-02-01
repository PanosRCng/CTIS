import json

from Core.IO import IO



class Resources:

    __instance = None


    def __init__(self):

        if Resources.__instance is not None:
            return

        Resources.__instance = self
        self.__setup()


    @staticmethod
    def __get_instance():

        if Resources.__instance is None:
            Resources()

        return Resources.__instance


    @staticmethod
    def get(key):
        return Resources.__get_instance().__get(key)


    def __setup(self):

        self.__folder = 'resources'

        self.__contents = self.__load()




    def __load(self):

        return {
            'indices_settings': self.__load_resource('indices_settings'),
            'stopwords_el': self.__load_resource('stopwords_el'),
            'stopwords_en': self.__load_resource('stopwords_en'),
        }


    def __load_resource(self, resource_filename):

        resource_path = IO.path(self.__folder, resource_filename + '.json')

        with open(resource_path) as file:
            contents = json.load(file)

            return contents


    def __get(self, key):

        if key in self.__contents:
            return self.__contents[key]

        return None

