from typing import List

import hashlib


class Shingle:
    ShingleSize = 2

    @classmethod
    def get_shingles_with_sentence(cls, text):
        hash_text = [hashlib.sha1(str(word).encode('utf-8')).hexdigest() for word in text]

        shingles_prew = [hash_text[word:word + cls.ShingleSize] for word in range(len(hash_text))][:-cls.ShingleSize + 1]
        shingles = [hashlib.sha1(str(hex(sum(list(map(lambda x: int(x, base=16), hash))))).encode('utf-8')).hexdigest() for hash in shingles_prew]

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