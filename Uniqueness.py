from typing import List, Dict


class Uniqueness:
    """
    Class for calculating the percentage of uniqueness
    """
    @classmethod
    def uniqueness_wroker(cls, shingles: List[List[str]] = None) -> float:
        if shingles is None:
            return 0.0

        uniqueness_percent = len(set(shingles[0]) & set(shingles[1])) / len(set(shingles[0]))

        return float(uniqueness_percent)

    @classmethod
    def uniqueness_document(cls, verifiable_document: Dict, phrase_compare: List[Dict]) -> Dict:
        uniqueness_percent = {}
        if phrase_compare:
            for doc in phrase_compare:
                union = set(verifiable_document['hashes']) & set(doc['hashes'])
                percent = len(union) / len(set(verifiable_document['hashes']))
                uniqueness_percent[str(doc['doc_id'])] = {'percent': (percent) * 100, "hashes": list(union)}

            return {'document_id': verifiable_document['doc_id'], 'result': uniqueness_percent}
        else:
            return cls.uniqueness_document_empty(verifiable_document)
    @classmethod
    def uniqueness_document_empty(cls, verifiable_document: Dict):
        return {'document_id': verifiable_document['doc_id'],
                'result': {str(verifiable_document['doc_id']):
                               {'percent': 0.0, "hashes": list(verifiable_document['hashes'])}}}