Anti-plagiarism
===========
---

System for detecting borrowed text fragments in an indexed collection of documents


## Installation

___

1) Python 3.8 [install](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
2) ```python3.8 -m venv env```
3) ```source env/bin/activate```
5) ```python3.8 -m pip install -r requirements.txt```
6) ```bash base_command_{ind}.sh```

## Note

Лучший способ развернуть систему, это зайти в Dockerfile и выполнять команды которые содержатся в нем.  
```config.py``` Содержит конфигурационные данные системы. 
```python
PSQL_USER = "user_document" 
PSQL_PASSWORD = "1111"
PSQL_HOST = "127.0.0.1"
PSQL_PORT = 5432
PSQL_DATABASE = "test_documents"
PSQL_TABLE_SHINGLES = "ip_term_shingles" # Имя таблицы с шинглами
PSQL_TABLE_TEXT_PAGE = "in_pages" # Имя таблицы с текстом файлов
# Креды для подключения к postgres SQL 

JSON_DATA_FILE_PATH = "convert_symbols_data.json" # файл с входными данными
SHINGLE_SIZE = 3 # Шаг шингла с которым будет проходить поиск заимствований
COUNT_CONJUNCTION = 3 # Кол-во фильтраций документов для поиска уникальных заимствований
```
Для запуска одного из типов работы системы используете файлы base_coomand_{}.sh

Результат работы системы выводится в файл ```output.json``` в формате json объекта с понятной структурой  

Пример вывода:
```json
[
  {
    "document_id": 10002,
    "result": {
      "10003": {
        "percent": 0.7692307692307693,
        "hashes": [
          "168eaf9e834e38839b7627f9326b7c73"
        ],
        "hashes_id": [
          3012
        ]
      }
    }
  },
  {
    "document_id": 10003,
    "result": {
      "10002": {
        "percent": 0.7299270072992701,
        "hashes": [
          "168eaf9e834e38839b7627f9326b7c73"
        ],
        "hashes_id": [
          3142
        ]
      }
    }
  }
]
```
Сам ответ является списком документов для которых проходила реиндексация
+ Поле ```document_id``` содержит id документа для которого проходила реиндексация
+ Поле ```result``` содержит словарь где ключем является ```doc_id``` документов в которых нашлись совпадения
+ Поле ```percent``` Содержит % сходства документов
+ Поле ```hashes``` Содержит список хэшей шинглов по которым нашлось сходство
+ Поле ```hashes_id``` Содержит id фраз/шинглов по которым нашлось сходство

Если реиндексировать документ по каким-то причинам не удалось, это тоже запишется в поле ```result``` как ```error```
где будет описана причина, а обработка продолжится дальше.

При вызове base_command_4.sh файл будет содержать список стоп слов.
