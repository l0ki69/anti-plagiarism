import os
from typing import List

from Converter import Сonverter, MisprintException
from Shingle import Shingle
from Uniqueness import Uniqueness
from PSQL import PSQL
from config import SHINGLE_SIZE, COUNT_CONJUNCTION

psql = PSQL()


class Plahiarismhandler:
    """
    The class performs a full cycle of checking for similarity of texts
    """
    def __init__(self):
        self.psql = PSQL()
        self.shingle_worker = Shingle(int(SHINGLE_SIZE))

    def get_conver_text(self, text: str) -> List[str]:
        try:
            return Сonverter.convert_text(text)
        except MisprintException as e:
            return []

    def handler(self, text_1: str, text_2: str) -> tuple:

        simple_text_1 = self.get_conver_text(text_1)
        simple_text_2 = self.get_conver_text(text_2)

        shingle_1 = self.shingle_worker.get_shingles_with_text(simple_text_1)
        shingle_2 = self.shingle_worker.get_shingles_with_text(simple_text_2)

        print(shingle_1)
        print(shingle_2)

        shingle_hash_1 = [ph['hash'] for ph in shingle_1]
        shingle_hash_2 = [ph['hash'] for ph in shingle_2]

        result_percent = Uniqueness.uniqueness_wroker([shingle_hash_1, shingle_hash_2])

        return f"{(1.0 - result_percent) * 100} %", "Check success"

    def __conjunction_hashes(self, equal_phrase: List[dict]) -> List[dict]:
        if not equal_phrase:
            return []

        for count in range(0, COUNT_CONJUNCTION):
            # loop finds intersections of hashes in different documents and removes them
            if len(equal_phrase) < count + 1:
                break
            for hs in equal_phrase[count]['hashes']:
                for ind, equal in enumerate(equal_phrase):
                    if ind == 0:
                        continue
                    if hs in equal['hashes']:
                        equal['hashes'].remove(hs)

            for equal in list(equal_phrase):
                if len(equal['hashes']) == 0:
                    equal_phrase.remove(equal)

            equal_phrase = sorted(equal_phrase, key=lambda hs: len(hs["hashes"]), reverse=True)

        # We take 3 documents with the largest number of unique matches
        return equal_phrase[:3]

    def document_indexing(self, document_id: int) -> dict:
        """
        The method does the reindexing of one document
        :param document_id: int
        :return: dict
        """
        text = self.psql.get_text_document(document_id)
        simple_text = self.get_conver_text(text)
        shingles = self.shingle_worker.get_shingles_with_text(simple_text)

        shingle_hash = [sh['hash'] for sh in shingles]

        result_phrase = self.psql.get_shingles(shingle_hash ,SHINGLE_SIZE)
        hashes_id = {}
        for phrase in result_phrase:
            hashes_id[phrase['hash']] = phrase['id']

        equal_phrase_dict = {}
        for phrase in result_phrase:
            if phrase['size'] == SHINGLE_SIZE:
                if phrase['ip_id'] in equal_phrase_dict:
                    equal_phrase_dict[phrase['ip_id']].append(phrase['hash'])
                else:
                    equal_phrase_dict[phrase['ip_id']] = [phrase['hash']]

        if equal_phrase_dict:
            if document_id in equal_phrase_dict:
                equal_phrase_dict.pop(document_id)

            for doc_id in equal_phrase_dict.keys():
                equal_phrase_dict[doc_id] = self.shingle_worker.shingle_sorted(equal_phrase_dict[doc_id])

            equal_phrase = sorted(tuple(equal_phrase_dict.items()), key=lambda i: len(i[1]), reverse=True)
            equal_phrase = [{'doc_id': equal[0], 'hashes': equal[1]} for equal in equal_phrase]

            top_equal_unique_phrase = self.__conjunction_hashes(equal_phrase)

            # restore the intersection of phrases from documents in the original
            phrase_compare = []
            for doc in top_equal_unique_phrase:
                for equal in equal_phrase:
                    if equal['doc_id'] == doc['doc_id']:
                        phrase_compare.append({'doc_id': doc['doc_id'], 'hashes': equal['hashes']})

            result = Uniqueness.uniqueness_document({'doc_id': document_id, 'hashes': shingle_hash}, phrase_compare)

            for doc_id, res in result['result'].items():
                result['result'][doc_id]['hashes_id'] = []
                for hs in res['hashes']:
                    if hs in hashes_id:
                        result['result'][doc_id]['hashes_id'].append(hashes_id[hs])

            self.psql.remove_doc(document_id, SHINGLE_SIZE)

        else:
            result = Uniqueness.uniqueness_document_empty({'doc_id': document_id, 'hashes': shingle_hash})

        for sh in shingles:
            row = [document_id, str(sh['phrase']).upper(), sh['times'], SHINGLE_SIZE, sh['hash']]
            self.psql.insert_row(row)

        return result

    def documents_indexing(self, documents_id: List[int]) -> List[dict]:
        """
        The method reindexes the list of documents
        :param documents_id: List[int]
        :return: List[dict]
        """
        result = []
        for doc_id in documents_id:
            try:
                res = self.document_indexing(doc_id)
                result.append(res)
            except Exception as e:
                result.append({'document_id': doc_id, 'result': {'error': f'Failed to index document - {e}'}})

        return result

    def all_documents_indexing(self) -> List[dict]:
        """
        The method reindexes all documents from the in_pages table of documents
        :return: -> List[dict]
        """

        documents_id = self.psql.get_all_documents()

        result = self.documents_indexing(documents_id)

        return result

    def get_stop_words(self) -> List[str]:
        """
        The method returns a list of stop words
        :return: List[str]
        """
        return Сonverter.get_stop_words()