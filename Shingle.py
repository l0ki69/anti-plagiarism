from typing import List

import hashlib


class Shingle:
    """
    Class for converting simplified text to shingles
    """
    def __init__(self, shingle_size: int):
        self.shingle_size = shingle_size

    def get_shingles_with_sentence(self, text):
        hash_text = [hashlib.sha1(str(word).encode('utf-8')).hexdigest() for word in text]

        shingles_prew = [hash_text[word:word + self.shingle_size] for word in range(len(hash_text))][:-self.shingle_size + 1]
        shingles = [hashlib.sha1(str(hex(sum(list(map(lambda x: int(x, base=16), hash))))).encode('utf-8')).hexdigest() for hash in shingles_prew]

        return shingles

    def get_list_words(self, text: List[str]) -> List[List[str]]:
        return [sentence.split(' ') for sentence in text]

    def get_list_shingles(self, shingles: List[List[str]]):
        shingles_list = []
        for sentence in shingles:
            shingles_list.extend(sentence)
        return shingles_list

    def get_shingles_with_page(self, text_page: List[str]) -> List[str]:
        sentence_words = self.get_list_words(text_page)

        shingles_page = [self.get_shingles_with_sentence(text=sentence) for sentence in sentence_words]
        return self.get_list_shingles(shingles_page)