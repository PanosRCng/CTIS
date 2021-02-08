from abc import ABC, abstractmethod
import importlib


class ContextsCache(ABC):


    @staticmethod
    def create(config):

        ActionModule = importlib.import_module('Core.CTIS.ContextsCache.' + config['driver'])
        ActionClass = getattr(ActionModule, config['driver'])

        return ActionClass(config['name'])



    @abstractmethod
    def set(self, title, context):
        pass


    @abstractmethod
    def set_many(self, contexts_dict):
        pass


    @abstractmethod
    def get(self, titles):
        pass
