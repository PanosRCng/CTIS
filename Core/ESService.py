from elasticsearch import helpers

from Core.ES import ES
from Core.Logger import Logger
from Core.Resources import Resources




class ESService:


    @staticmethod
    def bulk_insert(index_name, data_generator):

        body = ({
            "_index": index_name,
            "_id": data['_id'],
            "text": data['text']
            #"_source": data,
        } for data in data_generator)

        helpers.bulk(ES.connection('es'), body, chunk_size=500, request_timeout=100)


    @staticmethod
    def get_by_id(index_name, id):

        body = {
            "query": {
                "terms": {
                    "_id": [id]
                }
            }
        }

        hits = ES.connection('es').search(index=index_name, body=body)['hits']['hits']

        if len(hits) == 0:
            return None

        return hits[0]


    @staticmethod
    def get_by_ids(index_name, ids):

        body = {
            "query": {
                "terms": {
                    "_id": ids
                }
            }
        }

        res = ES.connection('es').search(index=index_name, body=body)

        return res['hits']['hits']


    @staticmethod
    def get_all(index_name, query):

        for item in helpers.scan(ES.connection('es'), index=index_name, query=query):
            yield(item)


    @staticmethod
    def create_index(name):

        try:

            if ES.connection('es').indices.exists(name):
                Logger.log(__name__, 'index ' + name + ' already exists', type='warning')
                return True

            ES.connection('es').indices.create(index=name, body=Resources.get('indices_settings')[name])

        except Exception as ex:
            Logger.log(__name__, 'could not create index ' + name + '\t' + str(ex), type='error')
            return False

        return True


    @staticmethod
    def delete_index(name):

        try:

            if not ES.connection('es').indices.exists(name):
                Logger.log(__name__, 'index ' + name + ' does not exist', type='error')
                return False

            ES.connection('es').indices.delete(index=name)

        except Exception as ex:
            Logger.log(__name__, 'could not delete index ' + name + '\t' + str(ex), type='error')
            return False

