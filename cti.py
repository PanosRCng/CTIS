from time import sleep
import signal
import sys
from multiprocessing import Process
from multiprocessing import Pool
from functools import partial

from Core.Config import Config
from Core.Logger import Logger
from Core.CTIS.CTI import CTI
from Core.CTIS.ContextsCache.ContextsCache import ContextsCache
from Core.CTIS.SearchEngine import SearchEngine
from Core.WikipediaUtils import WikipediaUtils

from Core.SQLiteDict import SQLiteDict
from Core.ElasticSearch.ESService import ESService

import spacy
from flask import Flask, request, abort




server = Flask(__name__)

cti = CTI()

nlp = spacy.load(Config.get('CTI')['space_postag_model'])





@server.route('/', methods=['POST'])
def cti_route():

    try:

        req = request.get_json()

        context = req['context']

    except Exception as ex:
        abort(400)

    return handle_cti_request(context)


def handle_cti_request(context):

    terms = []

    for token in nlp(context):

        if token.pos_ not in ['NOUN', 'ADJ']:
            continue
        terms.append(token.text)

    if len(terms) == 0:
        return {}

    scored = {}

    if len(terms) == 1:

        for term in terms:
            scored[term] = cti.term_informativeness(term, context)

    else:

        with Pool(2) as p:
            for term, score in p.map(partial(cti_job, cti=cti, context=context), terms):
                scored[term] = score

    scored = dict(sorted(scored.items(), key=lambda item: item[1], reverse=True))

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

    while True:

        try:
            title = SQLiteDict.storage(config['storage_name']).popitem()[0]
        except KeyError:
            sleep(config['empty_storage_wait_seconds'])
            continue

        contexts_cache.set(title, search_engine.context(title))

        Logger.log(__name__, 'backed off search got context for: ' + title)

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

    for article in WikipediaUtils.get_articles(dump_directory, attributes=['title', 'context'], max_articles=10):
        contexts_cache.set(article['title'], article['context'])
        Logger.log(__name__, 'bootstrapping got context for: ' + article['title'])


def clear_knowledge_base():
    ESService.delete_index(Config.get('CTI')['knowledge_base']['query_cache']['name'])
    ESService.delete_index(Config.get('CTI')['knowledge_base']['contexts_cache']['name'])
    Logger.log(__name__, 'knowledge base is now empty')


