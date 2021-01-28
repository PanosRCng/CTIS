

class Wikipedia:


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


