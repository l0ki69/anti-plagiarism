Anti-plagiarism
===========
---

System for detecting borrowed text fragments in an indexed collection of documents


## Installation

___

1) Python 3.8 [install](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
5) ```python3.8 -m pip install -r requirements.txt```


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

# START
Для запуска системы, достаточно выполнить ```bash``` скрипт, который сам соберет докер образ и запустит его   
+ ```bash docker_runner.bash```

После запуска образа, появится возможность кодлючиться к:
```bash
HOST="http://127.0.0.1:5000"
```
Можно выполнять curl запросы, или взаимодействовать с системой с помощью браузера.
___
```/plagiarism```
```bash
curl "${HOST}/plagiarism"
```

result:
```json
{
  "add_document": "${HOST}/plagiarism/add_document/", 
  "get_report": "${HOST}/plagiarism/get_report/", 
  "get_stop_words": "${HOST}/plagiarism/get_stop_words/", 
  "reindex": "${HOST}/plagiarism/reindex/", 
  "reindex_all": "${HOST}/plagiarism/reindex_all/", 
  "reindex_list": "${HOST}/plagiarism/reindex_list/"
}
```
___
```/plagiarism/reindex/```   
Для запуска реиндексации конкретного документа:
```bash
curl "${HOST}/plagiarism/reindex/?size=SIZE&doc_id=DOC_Id"
```

Обязательные параметры: ```size```, ```doc_id```
___
```/plagiarism/reindex_list/```   
Для запуска реиндексации списка документов:
```bash
curl "${HOST}/plagiarism/reindex_list/?size=SIZE&docs_id=DOC_ID;DOC_ID"
```

Обязательные параметры: ```size```, ```docs_id```
___
```/plagiarism/reindex_all/```   
Для запуска реиндексации всей коллекции:
```bash
curl "${HOST}/plagiarism/reindex_list/?size=SIZE"
```

Обязательные параметры:```size```

Для получения статуса реиндексации всей коллекции нужно использовать ```doc_id``` = -1
___
```/plagiarism/get_report/```   
Для получения отчета обработки документа:
```bash
curl "${HOST}/plagiarism/get_report/?size=SIZE&doc_id=DOC_ID;DOC_ID"
```
___
```/plagiarism/add_document/```   
Для добавления новго документа:
```bash
curl -F "file=@PATH_FILE;filename=FILENAME" ""${HOST}/plagiarism/add_document/?size=SIZE"
```
Обязательные параметры: ```size```, ```file```

Для добовление нового документа в БД, необходимо выполнить ```POST``` запрос, и передать в нем файл.
___
```/plagiarism/get_stop_words/```   
Для получения списка стоп слов (список создается в файле ```report.json``` в ```container_dir```):
```bash
curl "${HOST}/plagiarism/get_stop_words/"
```
___

Сам ответ является списком документов для которых проходила реиндексация
+ Поле ```document_id``` Содержит id документа для которого проходила реиндексация
+ Поле ```result``` Содержит словарь где ключем является ```doc_id``` документов в которых нашлись совпадения
+ Поле ```percent``` Содержит % сходства документов
+ Поле ```hashes``` Содержит список хэшей шинглов по которым нашлось сходство
+ Поле ```hashes_id``` Содержит id фраз/шинглов по которым нашлось сходство
+ Поле ```html``` Содержит html страницу, на которой выделен заимствованный текст жирным шрифтом
Если реиндексировать документ по каким-то причинам не удалось, это тоже запишется в поле ```result``` как ```error```
где будет описана причина, а обработка продолжится дальше.

___
Парраметры:
+ ```size``` - обязательный параметр, длинна шингла для работы системы
+ ```action``` - обязательный параметр, действие, которое будет делать система
+ ```doc_id``` - id документа для реиндексации
+ ```docs_id``` - список id документов для реиндексации
___
Обработка нового документа делается через post запрос к которому вы прикрепите файл
Пример кода, который генерирует правильный post запрос:
```python
import requests

url = "http://localhost:5000/"
fp = open("path_to_dir/pdf.pdf", 'rb')
files = {"file": fp}
response = requests.post(f"{url}?size=3", files=files)
fp.close()
print(response.text)
```
Обязательно для добавления нового документ необходимо в параметрах запроса указать size!
___

Список действий:

+ ```/plagiarism/add_document/```   Добавление нового документа, post запрос
+ ```/plagiarism/get_report/```   Получение отчета о проделаной проверке
+ ```/plagiarism/get_stop_words/```    Получить список стоп слов
+ ```/plagiarism/reindex/```   Реиндексировать один существующий документ
+ ```/plagiarism/reindex_all/```   Реиндексировать всю коллекцию документов
+ ```/plagiarism/reindex_list/```   Реиндексировать список документов
```