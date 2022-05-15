import os

from Converter import Сonverter, MisprintException
from Shingle import Shingle
from Uniqueness import Uniqueness


class Plahiarismhandler:
    """
    The class performs a full cycle of checking for similarity of texts
    """

    @classmethod
    def handler(cls, text_1: str, text_2: str) -> tuple:

        try:
            simple_text_1 = Сonverter.convert_text(text_1)
            simple_text_2 = Сonverter.convert_text(text_2)
        except MisprintException as e:
            return "100.0 %", str(e)

        shingle_worker = Shingle(int(os.getenv('SHINGLE_SIZE')))
        shingle_1 = shingle_worker.get_shingles_with_text(simple_text_1)
        shingle_2 = shingle_worker.get_shingles_with_text(simple_text_2)

        print(shingle_1)
        print(shingle_2)

        shingle_hash_1 = [ph['hash'] for ph in shingle_1]
        shingle_hash_2 = [ph['hash'] for ph in shingle_2]

        result_percent = Uniqueness.uniqueness_wroker([shingle_hash_1, shingle_hash_2])

        return f"{(1.0 - result_percent) * 100} %", "Check success"
