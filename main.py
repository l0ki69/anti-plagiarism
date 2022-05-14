from typing import List, Dict
import os
from dotenv import load_dotenv

from fuzzywuzzy import fuzz, process

from Converter import Сonverter
from Shingle import Shingle


def open_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    text_1 = open_file("text_1.txt")
    text_2 = open_file("text_2.txt")

    # text_1 = "Комментарий удален. Причина: данный аккаунт был удалён."
    # text_2 = "Комментарий удален. Причина: оскорбление пользователей."

    text_1 = "Конференция состоится завтра по адресу академии"
    text_2 = "Завтра по адресу академии состоится конференция"

    # text_1 = "Солнце светит ярко"
    # text_2 = "Солнце свитит ярко"

    print(fuzz.token_set_ratio(text_1, text_2))

    simple_page_1 = Сonverter.convert_text(text_1)
    simple_page_2 = Сonverter.convert_text(text_2)
    print(fuzz.token_set_ratio(simple_page_1, simple_page_2))
    # for sentence in simple_page_1:
    #     a = process.extract(sentence, simple_page_2, limit=2)
    #     print('-' * 300)
    #     print(f" sentence = {sentence}\n similar = {a}")
    #     print('-' * 300)

    shingle_1 = Shingle.get_shingles_with_page(simple_page_1)
    shingle_2 = Shingle.get_shingles_with_page(simple_page_2)

    print(shingle_1)
    print(shingle_2)

    sim = len(set(shingle_1) & set(shingle_2)) / len(set(shingle_1))

    print(sim)