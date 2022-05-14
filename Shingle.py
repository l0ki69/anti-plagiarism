from typing import List, Tuple

import hashlib
from itertools import permutations


class ShingleException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TextIsShort(ShingleException):
    def __init__(self):
        message = "Text is too short"
        super().__init__(message)


class Shingle:
    """
    Class for converting simplified text to shingles
    """
    def __init__(self, shingle_size: int):
        self.shingle_size = shingle_size

    def get_shingles_with_sentence(self, text):
        hash_text = [hashlib.sha1(str(word).encode('utf-8')).hexdigest() for word in text]

        shingles_prew = [hash_text[word:word + self.shingle_size] for word in range(len(hash_text))][:-self.shingle_size + 1]

        shingles_permutations = []
        # loop makes all possible permutations of phrases
        for phrase in shingles_prew:
            for permutation in self.get_permutations():
                shing = ""
                for permut in permutation:
                    shing += phrase[int(permut)]

                shingles_permutations.append(hashlib.sha1(str(shing).encode('utf-8')).hexdigest())

        return shingles_permutations

    def get_list_words(self, text: List[str]) -> List[List[str]]:
        return [sentence.split(' ') for sentence in text]

    def get_list_shingles(self, shingles: List[List[str]]):
        shingles_list = []
        for sentence in shingles:
            shingles_list.extend(sentence)
        return shingles_list

    def get_shingles_with_text(self, text: List[str]) -> List[str]:
        sentence_words = self.get_list_words(text)

        shingles_text = [self.get_shingles_with_sentence(text=sentence) for sentence in sentence_words]

        if shingles_text:
            if not shingles_text[0]:
                raise TextIsShort
        return self.get_list_shingles(shingles_text)

    def get_permutations(self) -> List[Tuple[str]]:
        return [permutation for permutation in permutations("".join([str(i) for i in range(self.shingle_size)]))]