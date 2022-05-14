import os

from Converter import Сonverter
from Shingle import Shingle
from Uniqueness import Uniqueness


class Plahiarismhandler:
    """
    The class performs a full cycle of checking for similarity of texts
    """

    @classmethod
    def handler(cls, text_1: str, text_2: str) -> float:
        simple_page_1 = Сonverter.convert_text(text_1)
        simple_page_2 = Сonverter.convert_text(text_2)

        shingle_worker = Shingle(int(os.getenv('SHINGLE_SIZE')))
        shingle_1 = shingle_worker.get_shingles_with_page(simple_page_1)
        shingle_2 = shingle_worker.get_shingles_with_page(simple_page_2)

        print(shingle_1)
        print(shingle_2)

        result_percent = Uniqueness.uniqueness_wroker((shingle_1, shingle_2))

        return result_percent
