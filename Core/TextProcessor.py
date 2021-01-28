from sentence_splitter import split_text_into_sentences



class TextProcessor:


    @staticmethod
    def split_sentences(text, language='el'):
        return split_text_into_sentences(text=text, language=language)


    @staticmethod
    def remove_word_dividers(text):
        return text.translate(str.maketrans("\t\r\n", "   "))


    @staticmethod
    def remove_intonations(text):
        return text.translate(str.maketrans("άέήίόύώϊΐϋΰ", "αεηιουωιιυυ"))

    @staticmethod
    def remove_numbers(text):
        return text.translate(str.maketrans("0123456789", "          "))


    @staticmethod
    def remove_symbols(text):
        return text.translate(str.maketrans("&*@\^\"%+-=#$|_~", "               "))


    @staticmethod
    def remove_punctuations(text):
        return text.translate(str.maketrans("’'[](){}⟨⟩:,،、‒-–.…!<>«»-?‘’“”'\";/⁄`", "                                    "))





