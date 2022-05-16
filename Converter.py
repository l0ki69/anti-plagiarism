from typing import List
import json
import os

import spacy
import ru_core_news_md
from spacy.lang.ru.examples import sentences
# spacy.cli.download("ru_core_news_md")

from config import JSON_DATA_FILE_PATH


class СonverterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MisprintException(СonverterException):
    def __init__(self):
        message = "The number of misprint is more than 90%"
        super().__init__(message)


class FileNotFound(СonverterException):
    def __init__(self, file_name: str):
        message = f"File - {file_name} not exists"
        super().__init__(message)


class Сonverter:
    """
    Class for converting raw text to simplified
    """

    nlp = spacy.load('ru_core_news_md')
    stop_words = nlp.Defaults.stop_words

    exception_characters = []  # Characters to be removed
    equivalent_symbols = []  # Equivalent symbols

    @classmethod
    def load_json_conver_data(cls):
        file_name = JSON_DATA_FILE_PATH
        if not os.path.exists(file_name):
            raise FileNotFound(file_name)
        with open(file_name, 'r') as f:
            js = json.load(f)
            cls.exception_characters = js['exception_characters']
            cls.equivalent_symbols = js['equivalent_symbols']

            for not_stop_word in js['not_stop_words']:
                cls.stop_words.discard(not_stop_word['word'])

            for stop_word in js['stop_words']:
                cls.stop_words.add(stop_word['word'])

    @classmethod
    def convert_text(cls, text: str) -> List[str]:
        cls.load_json_conver_data()

        text = text.lower()
        for char in cls.exception_characters:
            text = text.replace(char['symbol'], '')

        for symbol in cls.equivalent_symbols:
            text = text.replace(symbol['en'], symbol['ru'])

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

                if token.text in cls.stop_words:
                    continue

                if token.text == token.lemma_ and token.pos_ == 'VERB':
                    count_misprint += 1

                simple_text += token.lemma_ + ' '
                # print(f"text = {token.text} | token.pos_ = {token.pos_} | token.tag = {token.tag_} |"
                #       f"token.dep_ = {token.dep_} | token.vocab = {token.vocab.lang} | "
                #       f"lemma = {token.lemma} | token.lemma_ = {token.lemma_}")
            if simple_text.strip():
                simple_sentence.append(simple_text.strip())

            if count_misprint / len(text.split(' ')) > 0.9:
                raise MisprintException

        return simple_sentence

    @classmethod
    def get_stop_words(cls):
        return list(cls.stop_words)