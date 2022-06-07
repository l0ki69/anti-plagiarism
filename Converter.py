import copy
from typing import List
import json
import os

import spacy
from spacy.lang.ru.examples import sentences

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
    separator_symbols = []
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

            cls.separator_symbols = js['separator_symbols']

    @classmethod
    def convert_text(cls, text: str):
        cls.load_json_conver_data()

        text = text.lower()
        text_copy = copy.copy(text)

        for sep in cls.separator_symbols:
            text = text.replace(sep['symbol'], ' ')

        text = cls.del_duplication_symbols(text)

        for char in cls.exception_characters:
            text = text.replace(char['symbol'], '')

        for symbol in cls.equivalent_symbols:
            text = text.replace(symbol['en'], symbol['ru'])

        for number in range(0, 10):
            text = text.replace(str(number), '')

        result_sentence = []
        for sentence in text.split('.'):
            if sentence not in [' ', '']:
                sentence = cls.del_duplication_symbols(sentence.strip())
                result_sentence.append(sentence.strip())

        simple_sentence = []
        count_misprint = 0
        position_words = {}
        position_text = 0
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

                if token.text in text_copy:
                    start = text_copy.find(token.text, position_text, len(text_copy))
                    position_text = start
                    if token.lemma_ in position_words:
                        position_words[token.lemma_].append({'start': start, 'end': start + len(token.text)})
                    else:
                        position_words[token.lemma_] = [{'start': start, 'end': start + len(token.text)}]

                simple_text += token.lemma_ + ' '
                # print(f"text = {token.text} | token.pos_ = {token.pos_} | token.tag = {token.tag_} |"
                #       f"token.dep_ = {token.dep_} | token.vocab = {token.vocab.lang} | "
                #       f"lemma = {token.lemma} | token.lemma_ = {token.lemma_}")
            if simple_text.strip():
                simple_sentence.append(simple_text.strip())

            if count_misprint / len(text.split(' ')) > 0.9:
                raise MisprintException

        return simple_sentence, position_words

    @classmethod
    def get_stop_words(cls):
        return list(cls.stop_words)

    @classmethod
    def del_duplication_symbols(cls, text: str) -> str:
        while " " * 2 in text:
            text = text.replace(" " * 2, " ")
            text = text.replace("." * 2, ".")

        return text
