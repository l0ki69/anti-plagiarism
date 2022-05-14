from typing import List

import spacy
import ru_core_news_md
# spacy.cli.download("ru_core_news_md")

from spacy.lang.ru.examples import sentences


class СonverterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MisprintException(СonverterException):
    def __init__(self):
        message = "The number of misprint is more than 90%"
        super().__init__(message)


class Сonverter:
    """
    Class for converting raw text to simplified
    """
    exception_characters = [',', ':', ';', '\'', '\"', '?', '!', '/', '\\', '|', '@', '#', '$', '%', '^', '&', '*',
                            '(', ')', '_', '+', '=', '[', ']', '{', '}', '`', '~', '№', '<', '>', '–', '-']

    equivalent_symbols = [('е', 'e'), ('т', 't'), ('о', 'o'), ('р', 'p'), ('а', 'a'), ('н', 'h'), ('к', 'k'),
                          ('х', 'x'), ('с', 'c'), ('в', 'b'), ('м', 'm')]

    nlp = spacy.load('ru_core_news_md')
    @classmethod
    def convert_text(cls, text: str) -> List[str]:
        text = text.lower()
        for char in cls.exception_characters:
            text = text.replace(char, '')

        for symbol in cls.equivalent_symbols:
            text = text.replace(symbol[1], symbol[0])

        for number in range(0, 10):
            text = text.replace(str(number), '')

        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('  ', ' ')

        result_sentence = []
        for sentence in text.split('.'):
            if sentence != ' ':
                result_sentence.append(sentence.strip())

        simple_sentence = []
        count_misprint = 0
        for sentence in result_sentence:
            doc = cls.nlp(sentence)
            simple_text = ''
            for token in doc:
                if token.tag_ in ['SCONJ', 'ADP', 'CCONJ']:
                    continue

                if token.text == token.lemma_ and token.pos_ == 'VERB':
                    count_misprint += 1

                simple_text += token.lemma_ + ' '
                # if token.text in ['дила', 'дела']:
                #     print(f"text = {token.text} | token.pos_ = {token.pos_} | token.tag = {token.tag_} |"
                #           f"token.dep_ = {token.dep_} | token.vocab = {token.vocab.lang} | "
                #           f"lemma = {token.lemma} | token.lemma_ = {token.lemma_}")
            if simple_text.strip():
                simple_sentence.append(simple_text.strip())

            if count_misprint / len(text.split(' ')) > 0.9:
                raise MisprintException

        return simple_sentence