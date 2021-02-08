import json

import wikipedia



class SearchEngine:


    def __init__(self):
        wikipedia.set_lang("el")


    def contexts_titles(self, term):
        return json.dumps(wikipedia.search(term, results=10, suggestion=False))


    def context(self, title):

        context = ''

        try:
            context = wikipedia.summary(title, sentences=1, chars=0, auto_suggest=False, redirect=False)
        except Exception as ex:
            pass

        return context


    def contexts(self, titles):

        contexts = {}

        for title in titles:
            contexts[title] = self.context(title)

        return contexts

