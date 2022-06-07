Anti-plagiarism
===========
---

System for detecting borrowed text fragments in an indexed collection of documents


## Installation

___

1) Python 3.8 [install](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
5) ```python3.8 -m pip install -r requirements.txt```
6) ```bash base_command_{ind}.sh```

## Note
 
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
COUNT_CONJUNCTION = 3 # Кол-во фильтраций документов для поиска уникальных заимствований
```

Результат работы системы выводится в файл ```container_dir/report_dir/doc_{doc_id}.json``` в формате json объекта с понятной структурой  
Также генерируется файл ```.html```, в котором выделены жирным шрифтом заимствованные фрагменты.
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
___

Запуск системы без образа:
```bash
SIZE=5 # - длинна шингла
ACTION=4 # - номер действия
temp_param={} # - дополнительные парраметры в зависимости от action
python3.8 main.py ${SIZE} ${ACTION} ${temp_param}
```

___
# Развернуть докер образ:
```bash
docker build -f Dockerfile -t ant_test:build .
docker run -v {path_to_project}/anti-plagiarism/container_dir/:/anti-plagiarism/container_dir --name ant_dir -d -p 5000:5000 ant_test:build
```
Когда докер запущен можно обращаться к системе через http запросы.

P.S. Докер собирается из папки проекта, там же и находится ```volume``` = container_dir   
В ней же расположен конфигурационный файл, который хранит в себе креды для подключения к БД, и другие мета файлы
___
Парраметры:
+ ```size``` - обязательный параметр, длинна шингла для работы системы
+ ```action``` - обязательный параметр, действие, которое будет делать система
+ ```doc_path``` - путь/имя документа для обработки (документ должен лежать в ```volume``` в папке ```container_dir```)
+ ```doc_id``` - id документа для реиндексации
+ ```docs_id``` - список id документов для реиндексации
___
action_list:
+ 0 - обработка документа
+ 1 - реиднексация одного документа
+ 2 - реидексация списка документов
+ 3 - реиндексация всей коллекции документов
+ 4 - возвращать словарь стоп слов (единственный action, который отработает без коннекта к БД)
___
Примеры запросов:
```bash
BASE_URL="http://localhost:5000/"
SIZE=5
```
___
Обработка нового документа
```bash
ACTION=0
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}&doc_path=pdf.pdf"
```
___
Реиндексация существующего документа
```bash
ACTION=1
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}&doc_id=10005"
```
___
Реиндексация списка документов
```bash
ACTION=2
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}&docs_id=10005,10006,100007,100000"
```
___
Реиндексация всей коллекции документов
```bash
ACTION=3
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}"
```
___
Получение списка стоп слов 
```bash
ACTION=4
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}"
```