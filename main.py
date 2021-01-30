import time
import spacy
from multiprocessing import Pool
from multiprocessing import Process
from functools import partial

from Core.IO import IO
from Core.Wikipedia import Wikipedia
from Core.CTIS.CTI import CTI
from Core.Tokenizer import Tokenizer

from Core.CTIS.SearchEngine import SearchEngine




def get_articles(wikipedia_directory, max_articles, min_length=None):

    sc = 0

    for file in IO.files_in_directory_tree(wikipedia_directory):

        for doc in Wikipedia.extract_documents(file):

            if (min_length is not None) and (len(doc) < min_length):
                continue

            lines = doc.split('\n')
            title = lines[0]
            context = lines[1]

            print('##' + title + '##')
            print('##' + context + '##')

            #with open(Data.get('articles/article_' + str(sc) + '.txt'), 'a') as out:
            #    out.write(doc)

            sc += 1

            if sc >= max_articles:
                return


def featured_context_set(term):

    print(term)

    for title in wikipedia.search(term, results=10, suggestion=False):

        context = ''

        try:
            context = wikipedia.summary(title, sentences=1, chars=0, auto_suggest=False, redirect=False).split('\n')
            print(title)
            print(context)
            print('\n')
        except Exception as ex:
            pass


def test_job(term, cti, context):

    return term, cti.term_informativeness(term, context)





def main():

    '''
    context = 'Ο ιός είναι παθογενετικός παράγοντας που δρα μολύνοντας τα κύτταρα ενός οργανισμού, ενσωματώνοντας το γενετικό του υλικό στο γονιδίωμα αυτών και χρησιμοποιώντας για τον πολλαπλασιασμό του τους μηχανισμούς αντιγραφής, μεταγραφής και μετάφρασης του κυττάρου, όπως και τα περισσότερα ένζυμα που χρειάζεται για την επιβίωση του.'

    terms = ['ιός', 'παθογενετικός']


    #tokenizer = Tokenizer()
    #terms = list(set(tokenizer.tokenize(context, tokens_min_length=2)))


    terms = []
    nlp = spacy.load("el_core_news_md")
    for token in nlp(context):

        if token.pos_ not in  ['NOUN', 'ADJ']:
            continue
        terms.append(token.text)

    print(terms)
    terms = terms[:2]

    start_time = time.time()

    cti = CTI()

    scored = {}

    for term in terms:
        scored[term] = cti.term_informativeness(term, context)


    #with Pool(2) as p:
    #    for term, score in p.map(partial(test_job, cti=cti, context=context), terms):
    #        scored[term] = score

    scored = dict(sorted(scored.items(), key=lambda item: item[1], reverse=True))

    for term, cti in scored.items():
        print(term, cti)
    '''

    get_articles('/home/panos/Downloads/greek_wiki/extracted', max_articles=1, min_length=2000)


    search_engine = SearchEngine()

    res = search_engine.context('Χαράλαμπος Ταϊγανίδης')

    print(res)

    #print(time.time() - start_time)













if __name__ == '__main__':
    main()


