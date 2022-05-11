from typing import List, Dict

import spacy
import hashlib
from spacy.lang.ru.examples import sentences
from fuzzywuzzy import fuzz, process


class Сonverter:
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
        for sentence in result_sentence:
            doc = cls.nlp(sentence)
            simple_text = ''
            for token in doc:
                if token.tag_ in ['SCONJ', 'ADP', 'CCONJ']:
                    continue

                simple_text += token.lemma_ + ' '

                # print(f"text = {token.text} | token.tag = {token.tag_}")
                # print(f"text = {token.text} | token.pos_ = {token.pos_} | token.tag = {token.tag_} |"
                #       f"token.dep_ = {token.dep_} | token.vocab = {token.vocab.lang} | "
                #       f"lemma = {token.lemma} | token.lemma_ = {token.lemma_}")
            if simple_text.strip():
                simple_sentence.append(simple_text.strip())
        return simple_sentence


class Shingle:
    ShingleSize = 2

    @classmethod
    def get_shingles_with_sentence(cls, text):
        hash_text = [hashlib.sha1(str(word).encode('utf-8')).hexdigest() for word in text]

        shingles_prew = [hash_text[word:word + cls.ShingleSize] for word in range(len(hash_text))][:-cls.ShingleSize]

        shingles = [hashlib.sha1(str("".join(hash)).encode('utf-8')).hexdigest() for hash in shingles_prew]

        return shingles

    @classmethod
    def get_list_words(cls, text: List[str]) -> List[List[str]]:
        return [sentence.split(' ') for sentence in text]

    @classmethod
    def get_list_shingles(cls, shingles: List[List[str]]):
        shingles_list = []
        for sentence in shingles:
            shingles_list.extend(sentence)
        return shingles_list

    @classmethod
    def get_shingles_with_page(cls, text_page: List[str]):
        sentence_words = cls.get_list_words(text_page)

        shingles_page = [cls.get_shingles_with_sentence(sentence) for sentence in sentence_words]

        return cls.get_list_shingles(shingles_page)


def open_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


if __name__ == '__main__':
    text_1 = open_file("text_1.txt")
    text_2 = open_file("text_2.txt")

    # text_1 = "Комментарий удален. Причина: данный аккаунт был удалён."
    # text_2 = "Комментарий удален. Причина: оскорбление пользователей."

    simple_page_1 = Сonverter.convert_text(text_1)
    simple_page_2 = Сonverter.convert_text(text_2)

    # for sentence in simple_page_1:
    #     a = process.extract(sentence, simple_page_2, limit=2)
    #     print('-' * 300)
    #     print(f" sentence = {sentence}\n similar = {a}")
    #     print('-' * 300)

    shingle_1 = Shingle.get_shingles_with_page(simple_page_1)
    shingle_2 = Shingle.get_shingles_with_page(simple_page_2)

    print(shingle_1)
    print(shingle_2)

    sim = len(set(shingle_1) & set(shingle_2)) / len(set(shingle_1) | set(shingle_2))

    print(sim)