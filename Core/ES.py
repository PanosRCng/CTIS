import os

from elasticsearch import Elasticsearch
from Core.Config import Config




class ES:

    __instance = None


    def __init__(self):

        if ES.__instance is not None:
            return

        ES.__instance = self
        self.__setup()



    @staticmethod
    def __get_instance():

        if ES.__instance is None:
            ES()

        return ES.__instance


    @staticmethod
    def connection(connection_name):
        return ES.__get_instance().__connection(connection_name)



    def __setup(self):
        self.__conns = {}
        self.__configs = Config.get('elasticsearch')


    def __connection(self, connection_name):

        if connection_name not in self.__configs:
            return None

        return self.__get_conn(connection_name)


    def __get_conn(self, connection_name):

        pid_conn_name = self.__pid_connection_name(connection_name)

        if self.__conn_exists(pid_conn_name):
            return self.__conns[pid_conn_name]

        connection = self.__open_conn(self.__configs[connection_name])

        if connection is None:
            return None

        self.__conns[pid_conn_name] = connection

        return self.__conns[pid_conn_name]


    def __conn_exists(self, connection_name):

        if connection_name not in self.__conns:
            return False

        if self.__conns[connection_name] is None:
            return False

        return True


    def __open_conn(self, config):

        connection = None

        try:
            connection = Elasticsearch([
                {
                    'host': config['host'],
                    'port': config['port'],
                    'url_prefix': config['url_prefix']
                }
            ])
        except Exception as ex:
            print(ex)

        if connection.ping() is False:
            return None

        return connection


    def __pid_connection_name(self, connection_name):
        return connection_name + '_' + str(os.getpid())


