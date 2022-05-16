from typing import List, Dict
import os
import sys
import json
from dotenv import load_dotenv

from Plahiarismhandler import Plahiarismhandler, psql


def open_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # args = sys.argv
    # file_name_1 = args[1]
    # file_name_2 = args[2]

    file_name_1 = "text_1.txt"
    file_name_2 = "text_2.txt"

    text_1 = open_file(file_name_1)
    text_2 = open_file(file_name_2)

    # text_1 = "Конференция состоится завтра по адресу академии"
    # text_2 = "Завтра по адресу академии состоится конференция"

    # text_1 = "Солнце светит ярко"
    # text_2 = "Солнце свитит ярко"

    # text = psql.get_text_document(10002)
    #
    # shingles = psql.get_shingles(['04647cfbae3ddee9bff56c4a21a2bfe9', '8fee5e7941ce7e8e7c5c30375279885c'])
    # print(f"shingles = {shingles}")
    # psql.insert_row()

    handler = Plahiarismhandler()
    # result = handler.handler(text_1, text_2)
    result = handler.document_indexing(10003)

    print(result)

    with open('output.out', 'w') as out:
        json.dump(result, out)