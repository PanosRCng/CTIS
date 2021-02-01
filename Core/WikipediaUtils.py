from Core.IO import IO



class WikipediaUtils:


    @staticmethod
    def get_articles(wikipedia_directory, attributes=['title', 'context', 'text'], max_articles=None, min_length=None):

        sc = 0

        for file in IO.files_in_directory_tree(wikipedia_directory):

            for doc in WikipediaUtils.extract_documents(file):

                if (min_length is not None) and (len(doc) < min_length):
                    continue

                article = WikipediaUtils.__extract_article(doc)

                data = {}

                for attribute in attributes:
                    data[attribute] = article[attribute]

                yield data

                sc += 1

                if (max_articles is not None) and (sc >= max_articles):
                    return


    @staticmethod
    def extract_documents(wiki_file):

        docs = []

        with open(wiki_file) as file:

            doc = ''

            for line in file.readlines():

                if line.strip() == '':
                    continue

                if '<doc' in line:
                    continue
                elif '</doc>' in line:
                    docs.append(doc)
                    doc = ''
                else:
                    doc += line

        return docs



    @staticmethod
    def __extract_article(doc):

        lines = doc.split('\n')
        title = lines[0]
        context = lines[1]
        text = '\n'.join(lines[1:])

        return {'title': title, 'context': context, 'text': text}

