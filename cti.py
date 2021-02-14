import sys
import signal
import os
from time import sleep
from multiprocessing import Process
from multiprocessing import Pool
from functools import partial

from Core.Config import Config
from Core.Logger import Logger
from Core.Data import Data
from Core.CTIS.CTI import CTI
from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.CTIS.SearchEngine import SearchEngine
from Core.WikipediaUtils import WikipediaUtils
from Core.SQLiteDict import SQLiteDict
from Core.ElasticSearch.ESService import ESService

from flask import Flask, request, abort




server = Flask(__name__)

cti = CTI()






@server.route('/', methods=['POST'])
def cti_route():

    try:

        req = request.get_json()

        terms = req['terms']
        context = req['context']

    except Exception as ex:
        abort(400)

    return handle_cti_request(terms, context)


def handle_cti_request(terms, context):

    if len(terms) == 0:
        return {}

    scored = {}

    if (Config.get('CTI')['max_processes_per_job'] == 1) or (len(terms) == 1):

        for term in terms:
            scored[term] = round(cti.term_informativeness(term, context), 2)

    else:

        with Pool(Config.get('CTI')['max_processes_per_job']) as p:
            for term, score in p.map(partial(cti_job, cti=cti, context=context), terms):
                scored[term] = score

    return scored



def signal_exit_handler(sig, frame):
    sys.exit(0)


def cti_job(term, cti, context):
    return term, cti.term_informativeness(term, context)


def backed_off_search():

    config = Config.get('CTI')['backed_off_search']

    contexts_cache = ContextsCache.create(Config.get('CTI')['knowledge_base']['contexts_cache'])
    search_engine = SearchEngine()

    Logger.log(__name__, 'backed off search process started')
    Logger.log(__name__, 'backed off search storage has ' + str(len(SQLiteDict.storage(config['storage_name']))) + ' items')

    c = 0

    while True:

        try:
            title = SQLiteDict.storage(config['storage_name']).popitem()[0]
        except KeyError:
            sleep(config['empty_storage_wait_seconds'])
            continue

        contexts_cache.set(title, search_engine.context(title))

        Logger.log(__name__, 'backed off search got context for: ' + title)

        c += 1
        if c > 30:
            c = 0
            Logger.log(__name__, 'backed off search storage has ' + str(len(SQLiteDict.storage(config['storage_name']))) + ' items')

        sleep(config['seconds_between_searches'])



def start_server():

    signal.signal(signal.SIGINT, signal_exit_handler)

    backed_off_search_process = None

    if Config.get('CTI')['knowledge_base']['on_miss_backoff']:
        backed_off_search_process = Process(target=backed_off_search)
        backed_off_search_process.start()

    config = Config.get('server')

    server.run(host=config['host'], port=config['port'], threaded=True)

    if Config.get('CTI')['knowledge_base']['on_miss_backoff']:
        backed_off_search_process.join()


def bootstrap_knowledge_base(dump_directory):

    Logger.log(__name__, 'bootstrapping knowledge base...')

    contexts_cache = ContextsCache.create(Config.get('CTI')['knowledge_base']['contexts_cache'])

    for article in WikipediaUtils.get_articles(dump_directory, attributes=['title', 'context']):
        contexts_cache.set(article['title'], article['context'])
        Logger.log(__name__, 'bootstrapping got context for: ' + article['title'])


def clear_knowledge_base():
    ESService.delete_index(Config.get('CTI')['knowledge_base']['query_cache']['name'])
    ESService.delete_index(Config.get('CTI')['knowledge_base']['contexts_cache']['name'])
    Logger.log(__name__, 'the knowledge base is now empty')


def clear_backedoff_storage():

    storage_path = Data.get(Config.get('CTI')['backed_off_search']['storage_name'])

    if os.path.isfile(storage_path):
        os.remove(storage_path)
        Logger.log(__name__, 'the backedoff search storage is now empty')
    else:
        Logger.log(__name__, 'the backedoff search storage is already empty')
