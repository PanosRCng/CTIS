from Core.Resources import Resources
from Core.TextProcessor import TextProcessor



class Tokenizer:


    def __init__(self, stopwords_el=True, stopwords_en=True):

        self.__stopwords = self.__load_stopwords(stopwords_el, stopwords_en)



    def __load_stopwords(self, el, en):

        stopwords = []

        if el is True:
            stopwords += Resources.get('stopwords_el')

        if en is True:
            stopwords += Resources.get('stopwords_en')

        return stopwords


    def tokenize(self, text, tokens_min_length=None):

        cl_text = text.lower()
        cl_text = TextProcessor.remove_punctuations(cl_text)
        cl_text = TextProcessor.remove_symbols(cl_text)
        cl_text = TextProcessor.remove_intonations(cl_text)
        cl_text = TextProcessor.remove_numbers(cl_text)
        cl_text = TextProcessor.remove_word_dividers(cl_text)

        return self.remove_stopwords( self.tokens(cl_text, tokens_min_length) )


    def tokens(self, text, tokens_min_length=None):

        if tokens_min_length is not None:
            return [token for token in text.split(' ') if token != '' and tokens_min_length <= len(token)]

        return [token for token in text.split(' ') if token != '']


    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.__stopwords]





