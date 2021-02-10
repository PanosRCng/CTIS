from math import log

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Core.CTIS.KnowledgeBase import KnowledgeBase



class CTI:


    def __init__(self):

        self.__knowledge_base = KnowledgeBase()
        self.__tfidf_vectorizer = TfidfVectorizer()



    def term_informativeness(self, term, context):

        I = 0

        U_f = self.__knowledge_base.featured_context_set(term)

        for j in range(len(U_f)):

            s = self.__semantic_relatedness(context, U_f[j])

            if j > 0:
                I = I + s / log(j + 1)
            else:
                I = I + s

        return I



    def __semantic_relatedness(self, context_i, context_j):

        tfidf_matrix = self.__tfidf_vectorizer.fit_transform([context_i, context_j])

        return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]


