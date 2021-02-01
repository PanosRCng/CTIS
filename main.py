import spacy
from multiprocessing import Pool
from functools import partial

from Core.Config import Config
from Core.WikipediaUtils import WikipediaUtils
from Core.CTIS.CTI import CTI

from Core.CTIS.ContextsCache.ContextsCache import ContextsCache

import time





def bootstrap_knowledge_base():

    contexts_cache = ContextsCache.create(Config.get('contexts_cache'))

    wikipedia_directory = '/home/panos/Downloads/greek_wiki/extracted'

    for article in WikipediaUtils.get_articles(wikipedia_directory, attributes=['title', 'context'], max_articles=10):
        contexts_cache.set(article['title'], article['context'])



def cti_job(term, cti, context):
    return term, cti.term_informativeness(term, context)




def main():


    context = 'Ο ιός είναι παθογενετικός παράγοντας που δρα μολύνοντας τα κύτταρα ενός οργανισμού, ενσωματώνοντας το γενετικό του υλικό στο γονιδίωμα αυτών και χρησιμοποιώντας για τον πολλαπλασιασμό του τους μηχανισμούς αντιγραφής, μεταγραφής και μετάφρασης του κυττάρου, όπως και τα περισσότερα ένζυμα που χρειάζεται για την επιβίωση του.'

    terms = ['ιός', 'παθογενετικός']


    #tokenizer = Tokenizer()
    #terms = list(set(tokenizer.tokenize(context, tokens_min_length=2)))


    terms = []
    nlp = spacy.load("el_core_news_md")
    for token in nlp(context):

        if token.pos_ not in ['NOUN', 'ADJ']:
            continue
        terms.append(token.text)

    #terms = terms[:2]

    start_time = time.time()


    scored = {}

    cti = CTI()

    with Pool(2) as p:
        for term, score in p.map(partial(cti_job, cti=cti, context=context), terms):
            scored[term] = score

    scored = dict(sorted(scored.items(), key=lambda item: item[1], reverse=True))


    for term, cti in scored.items():
        print(term, cti)


    print(time.time() - start_time)


    #bootstrap_knowledge_base()












if __name__ == '__main__':
    main()


