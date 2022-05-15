from typing import List, Dict
import os
import sys
from dotenv import load_dotenv

from Plahiarismhandler import Plahiarismhandler
from PSQL import PSQL


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

    psql = PSQL(user=os.getenv("PSQL_USER"),
                password=os.getenv("PSQL_PASSWORD"),
                host=os.getenv("PSQL_HOST"),
                port=os.getenv("PSQL_PORT"),
                database=os.getenv("PSQL_DATABASE"))

    # file_name_1 = "text_1.txt"
    # file_name_2 = "text_2.txt"

    text_1 = open_file(file_name_1)
    text_2 = open_file(file_name_2)

    # text_1 = "Конференция состоится завтра по адресу академии"
    # text_2 = "Завтра по адресу академии состоится конференция"

    # text_1 = "Солнце светит ярко"
    # text_2 = "Солнце свитит ярко"

    result = Plahiarismhandler.handler(text_1, text_2)

    print(result)

    with open('output.out', 'w') as out:
        out.write(f"result_percent = {result[0]}\n{result[1]}")