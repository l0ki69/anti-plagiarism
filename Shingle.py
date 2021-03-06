from typing import List, Tuple, Dict

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

    def get_shingles_with_sentence(self, sentence, position_words):
        hash_sentence = []
        for word in sentence:
            d_res = {"hash": hashlib.md5(str(word).encode('utf-8')).hexdigest(),
                     "word": word, "pos": {}}

            if word in position_words:
                if len(position_words[word]) > 0:
                    d_res["pos"] = position_words[word].pop(0)
                else:
                    d_res["pos"] = {'start': -1, 'end': -1}
            else:
                d_res['pos'] = {'start': -1, 'end': -1}
            hash_sentence.append(d_res)

        shingles_prew = [hash_sentence[word:word + self.shingle_size] for word in range(len(hash_sentence))][:-self.shingle_size + 1]

        shingles_permutations = []
        for phrase in shingles_prew:
            min_start = phrase[0]["pos"]["start"]
            max_end = phrase[0]["pos"]["end"]
            for ph in phrase:
                if -1 in [ph["pos"]['start'], ph["pos"]['end']]:
                    position = {"start": -1, "end": -1}
                    break
                if ph["pos"]['start'] < min_start:
                    min_start = ph["pos"]['start']
                if ph["pos"]['end'] > max_end:
                    max_end = ph["pos"]['end']
                position = {"start": min_start, "end": max_end}

            sorted_list_words = sorted(phrase, key=lambda hs: int(hs["hash"], base=16), reverse=True)

            hash = hashlib.md5(str("".join([word["hash"] for word in sorted_list_words])).encode('utf-8')).hexdigest()
            phrase = " ".join([word["word"] for word in sorted_list_words])
            shingles_permutations.append({"hash": hash, "phrase": phrase, "pos": position})

        return shingles_permutations

    def get_shingles_permutations(self, shingles_prew: List[List[str]]) -> List[str]:

        shingles_permutations = []
        # loop makes all possible permutations of phrases
        for phrase in shingles_prew:
            for permutation in self.get_permutations():
                shing = ""
                for permut in permutation:
                    shing += phrase[int(permut)]

                shingles_permutations.append(hashlib.md5(str(shing).encode('utf-8')).hexdigest())

        return shingles_permutations

    def get_shingles_with_text(self, text: List[str], position_words: Dict) -> List:
        sentence_words = [sentence.split(' ') for sentence in text]

        shingles = []
        for sentence in sentence_words:
            shingles.extend(self.get_shingles_with_sentence(sentence=sentence, position_words=position_words))

        if not shingles:
            raise TextIsShort

        temp_times = {}
        for sh in list(shingles):
            if sh['hash'] in temp_times:
                temp_times[sh['hash']] += 1
            else:
                temp_times[sh['hash']] = 1

        for sh in shingles:
            sh['times'] = temp_times[sh['hash']]

        return shingles

    def get_permutations(self) -> List[Tuple[str]]:
        return [permutation for permutation in permutations("".join([str(i) for i in range(self.shingle_size)]))]

    def shingle_sorted(self, shingles: List[str]) -> List[str]:
        return sorted(shingles, key=lambda hs: int(hs, base=16), reverse=True)