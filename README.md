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

Пример ответа:
```
{"report": {"document_id": 2147483580, "result": {"10002": {"percent": 100.0, "hashes": ["e74c67687b03d5cb8d414d2e77fd4f71", "685ba2c92dd5ab6c9f1c05139f980c00", "1052813f4411c7b0697a3d9ff21b2650", "3a456980cfe4250f5c7b37bcc669a4bf", "90190161f85a36d52c34716600cc977a", "90549b2856aafe6b8814a3dcb9a31855", "352a8798d8f5b449891e925ad9b654d3", "590ffc2bdfa59127cfeac286734befe4", "9d772a5eec5ad7e0b194c7c3c4bb91e6", "d0fcd023ba95cdf106e03bb07c780413", "b3c90b37bcbc4df2afac508e30de3db7", "58bdfc1faa61b075ef279f9d00c7798c", "253d09b6a4cceddfd63e4dbdcb924e74", "5943a2d97a9ccd032f33d283fec46519", "c8938945c678eca76e8850fec0222139", "83215ed6d400791a8b686582d49c3c99", "02d99ace405df35c83aaa64718157b6d", "9ea8e7bb09aa62351fe37d5c625c24fe", "811f3d8eb7d30f59ec8cb20e7fca6d0e", "fb88e82598675c0923e0eae9544194be", "7b3da55bf165c67e919b32cbd72ede01", "521e9ab727e8e4b8823e55c2d45758b3", "a47afc1e436f85caf4ff2a61ebceec84", "36a27da39bae63440d6a32f925e168b5", "60bad2bf09a9944fccd78b16956659fd", "951023a996e8af65396e9a314615bb57", "1b0031fcf826552ab01c0b422c613cc0", "146e0d600d1964e31b51d212d6e714ce", "bd00e9450a185e95ef017eb20369ad78", "fa45d714ba5a7569b76c03a4f43e121f", "b8c87c316d92506fd47f0fdc72481673", "37d7aa42c7353e76f757b547e6a1c427", "1582e8df597ae66f1227fd9cf0d6662c", "99890dfa7ab5a8a21f725b4142c98316", "ff68bd9e28087780c418d83ffcdeb009", "af91abc96b3599f92b623bd956ed8f01", "5501200cf3f3d37b2820716b069d85ab", "cf79342faf11e75ce3d2085c4ac5a5ca", "00d481d63081de532285e3964ba2af50", "c686c2ddabd3aed7cb2d500d1ebcb67a", "b5c376e2998964971b36809726c9f770", "24585ba33611db3d4ce364606e3e1969", "d9d296fc6e2192366abd5b67063ed85d", "f3a4988b018ff2b077d38bd699ad4652", "dead8d2630b7c93e96c31dcf89af9cb3", "e52c6e489215d806b30e5b8ecd044f45", "28c43485d4ec976f5e60a37774aaf3cc", "be2da46c112b4d4c01d55bd00238755d", "28decb675bb78b20b8213271f9523d56", "9be29a512e3391914945fd37b5a49ff5", "ab4a51eac42894c62150f1b4598fd393", "040ac8d618515e3aad8bb5e4fcb32c31", "d3c2b80f31f3b87ec2ee276e9fc60099", "c1fa11b4843801e8049cb7f8caae747e", "4f274739999c7fbce82f4fe52ee4a969", "18105e41a57b0c64c3e069c0a1eab4dd", "639f656c55d798cdc49851cb1cf9397e", "1bbe3507cb4019c52d67aef10de6754a", "865da9c262b169cc370f78d5009ba947", "0a2fb499caf98e3797d0eb5d613ad8a7", "90528058bd1f2acaeb04157d9c7cbf95", "0ceff1e41d17e3150c9fa6d7ff3f5acd", "1737320503bc6d62061958741f84808a", "afe4d0bd36922ef6d58145c7fb7fbd2b", "b74d0886655411375a3eec742ef5f99e", "6fd6127ab14e38b03b7748b77214acdd", "377d5f9f1539f28886788d86e74d8628", "63305f9c28111b14fbb293ec658a29f0", "168eaf9e834e38839b7627f9326b7c73", "9d9ef27c34d41bad65c08b690a347d4c", "131f1b91f21be40146b29bb82779d6f4", "b03fa4aa6666b53b745cb23851e136e2", "ad61b3612c1715e668e2d2ce3b8f4296", "45070da57de24cf3502b63de0dcd2cf2", "3fd830de99d30b4b14684618ff9c3d88", "dfb60d7e2f207cb838e0b8356d94810b", "3389ff9325b7d18abd2e996f462d0d46", "89388e34c953aafb7a9e2bc47ca95753", "e34e7fe065a5855ce2eb8ce8574529d1", "72d5bf01bad3cac97ae433f387553c48", "3275b8a3be730cad7fd01ee3e1b7d226", "5d04cd80aa5a5310c738538c6ac11b5e", "7e8ea28bb7f2e2725f4c56f95125bdc4", "1d6a511a5487d6bd98e439480e132b80", "f6a12f92dd25e16098df60c8dd9b5945", "1b2ed9a3d1796abc5c16ada5f13ec697", "b9d9ea2ce6fb0f1d848268f47e3e9af8", "b52ef61b55bf5f5e26917e7d3f591eee", "31e64fe1108951baf5e02b7258d3880c", "83f39ddf31fa72a4aa18b00b12f6477d", "89dc01daed2655e22bf806a7e0094acf", "4a0409dffc0f9a03525261adb0154074", "5a6b330465ca77989880b79962c86d77", "a5da65378c09fa75d540c511bae0ac41", "f588952f656869d1e381bbae308c8274", "e46d6c9c94349b4e6525a0f0f8054f1c", "677bcefdbe699c2ba459281f2fcc84ff", "c8067d85358a1cebcb9db99dfdafdc27", "2ca7784cd5d657a49f5eed245582c98c", "131e1813552e44300444032d9540f01d", "5214a98d389337df592aff5d08f01d66", "0eeca5ab20087c83c57f9ef3b7199d0e", "8980f6e17c77936c36eecffbb8f64459", "532b30bc87b4526a3fb4fc38ffec1af8", "a4ee8aad2fdffb2f57d77bc2a89ea6eb", "a3929a0b7b1af8bcbb232b64f9e8a695", "7d80add95ec9f51bc4db6b2ff3c322dc", "da281056c07c68a7da46116bef976dd6", "c1effc8107e9aa1ebf7c106a0f7f1033", "6f601650d1d07e8b51a450a55d70ee12", "52d7bdbd7620bea8d5165d8f93a1c496", "4d240816487bbf2da41c74553e576ac5", "1d979e510c70a650d161ac0b7e664960", "9dd0c5cb599b3802b6d4157c7c0ccd43", "0485c27f6caf0c1efe4de29e8592170b", "470fb223d0f87588def31bace720d6f4", "3852bbd40143ee1048fa6670ef1973bc", "dae0df514e78ee113a8edcc4953f1332", "7be9dd5eedf447562f53663226f4bdc1", "4062432ef5756bc3ba15792585b33072", "63ce6eb2598b0d5493b8ee126db8204c", "c638faac0b33c0fb1f2662909eb0d5b9", "538494e9f0ffd6d02f00e80e30fb8c64", "049e5c1a23602392dff1b4501c3813e0", "7725e9c85bee1fb3a6b89a8537fc2406", "930617bee0c9215ff04595d3de17c0e7", "00663176555912fafa9441205d21f39e", "755e6f671d1c6923fc45818b234551a3", "0a597e5647cffe07d87c33653bdece75", "eafce83b54f88b37b3dd1647314493ae"], "hashes_id": [59708, 59712, 59591, 59629, 59601, 59624, 59602, 59590, 59565, 59633, 59568, 59556, 59606, 59552, 59618, 59563, 59532, 59573, 59632, 59654, 59646, 59612, 59609, 59545, 59709, 59537, 59611, 59644, 59555, 59595, 59656, 59564, 59617, 59575, 59638, 59576, 59541, 59652, 59645, 59650, 59546, 59714, 59577, 59710, 59558, 59639, 59562, 59610, 59551, 59593, 59648, 59597, 59616, 59711, 59534, 59636, 59592, 59587, 59549, 59607, 59661, 59619, 59557, 59566, 59613, 59550, 59561, 59589, 59641, 59643, 59588, 59571, 59626, 59560, 59553, 59567, 59649, 59620, 59554, 59625, 59543, 59716, 59660, 59614, 59713, 59637, 59651, 59659, 59634, 59599, 59715, 59548, 59533, 59657, 59604, 59594, 59631, 59615, 59635, 59603, 59559, 59627, 59658, 59655, 59647, 59539, 59572, 59622, 59570, 59623, 59642, 59542, 59600, 59596, 59535, 59547, 59653, 59536, 59608, 59630, 59569, 59544, 59621, 59640, 59628, 59598, 59605, 59574, 59538, 59540]}}}, "html": "<!DOCTYPE html><html lang=\\"ru\\"><head><meta charset=\\"utf-8\\"><title></title></head><body><p><b>СЕГОДНЯ ИНФОРМАЦИЮ РАССМАТРИВАЮТ КАК ОДИН ИЗ ОСНОВНЫХ РЕСУРСОВ<br>РАЗВИТИЯ ОБЩЕСТВА, А ИНФОРМАЦИОННЫЕ СИСТЕМЫ И ТЕХНОЛОГИИ КАК СРЕДСТВО<br>ПОВЫШЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ И ЭФФЕКТИВНОСТИ РАБОТЫ. </b>без <b>СОВРЕМЕННЫХ<br>СИСТЕМ ОБРАБОТКИ ДАННЫХ ТРУДНО ПРЕДСТАВИТЬ ПЕРЕДОВЫЕ ПРОИЗВОДСТВЕННЫЕ<br>ТЕХНОЛОГИИ, УПРАВЛЕНИЕ ЭКОНОМИКОЙ НА ВСЕХ ЕЕ УРОВНЯХ, НАУЧНЫЕ<br>ИССЛЕДОВАНИЯ, ОБРАЗОВАНИЕ.\\\\</b>n<b>НЕЗАВИСИМО ОТ ОБЛАСТИ ЭКОНОМИКИ, В КОТОРОЙ РАБОТАЕТ ОРГАНИЗАЦИЯ,<br>ОСНОВНОЙ ЦЕЛЬЮ ВНЕДРЕНИЯ ИНФОРМАЦИОННЫХ СИСТЕМ ЯВЛЯЕТСЯ<br>ПЕРЕМЕЩЕНИЕ ИНФОРМАЦИОННОГО БАЗИСА ОРГАНИЗАЦИЙ В<br>СТРУКТУРИРОВАННУЮ, РАЗВИВАЮЩУЮСЯ В СООТВЕТСТВИИ С ЗАРАНЕЕ<br>НАМЕЧЕННЫМ ПЛАНОМ, СТРУКТУРУ, ЯВЛЯЮЩУЮСЯ ИСТОЧНИКОМ ИНФОРМАЦИИ И<br>ОТВЕЧАЮЩЕЙ ПОТРЕБНОСТЯМ БИЗНЕСА.\\\\</b>nв <b>СВЯЗИ С ТЕМ, ЧТО ПРОБЛЕМА ОРГАНИЗАЦИИ ПАРКОВОЧНЫХ МЕСТ В<br>КРУПНЫХ ГОРОДАХ – МЕГАПОЛИСАХ С КАЖДЫМ ГОДОМ СТАНОВИТСЯ АКТУАЛЬНЕЕ,<br>ОДНИМ ИЗ НАПРАВЛЕНИЙ БИЗНЕСА, В КОТОРОМ ИНФОРМАЦИОННЫЕ СИСТЕМЫ<br>НАХОДЯТ ВСЕ БОЛЬШЕЕ ПРИМЕНЕНИЕ, ЯВЛЯЕТСЯ ПАРКОВОЧНЫЙ БИЗНЕС.\\\\</b>nпрежде всего,такая <b>ПРОБЛЕМА ВЫЗВАНА НЕПРЕРЫВНЫМ УВЕЛИЧЕНИЕМ<br>КОЛИЧЕСТВА ТРАНСПОРТНЫХ СРЕДСТВ НА ДОРОГАХ ОБЩЕГО ПОЛЬЗОВАНИЯ.\\\\</b>n<b>АВТОМОБИЛЬНЫЕ ПАРКОВКИ ЯВЛЯЮТСЯ НЕОТЪЕМЛЕМОЙ ЧАСТЬЮ<br>СОВРЕМЕННОГО ГОРОДА, ОДНАКО ИХ НАЛИЧИЕ НЕ РЕШАЕТ ПРОБЛЕМУ СТИХИЙНОЙ<br>ПАРКОВКИ НА УЛИЦАХ МЕГАПОЛИСОВ. </b>одним из <b>ЭТАПОВ БОРЬБЫ С ВЫШЕУКАЗАННОЙ<br>ПРОБЛЕМОЙ ЯВЛЯЕТСЯ АВТОМАТИЗАЦИЯ ПАРКОВОК, КОТОРАЯ НЕ ПРОСТО УВЕЛИЧИВАЕТ<br>ЧИСЛО КЛИЕНТОВ, НО И ПРЕДСТАВЛЯЕТ СОБОЙ РАЦИОНАЛЬНОЕ И ЭКОНОМИЧЕСКИ<br>ВЫГОДНОЕ РЕШЕНИЕ, ПОВЫШАЮЩЕЕ КОНКУРЕНТОСПОСОБНОСТЬ ОРГАНИЗАЦИИ.\\\\</b>n<b>ПАРКОВОЧНЫЕ СИСТЕМЫ, РЕШАЮЩИЕ ВОПРОСЫ КОНТРОЛЯ </b>въезда–выезда, <b>РАСЧЕТА<br>СТОИМОСТИ ПАРКОВКИ, ОЦЕНКИ ЧИСЛА СВОБОДНЫХ МЕСТ УЖЕ ДАВНО ШИРОКО<br>РАСПРОСТРАНЕНЫ И ВНЕДРЕНЫ В ПОДАВЛЯЮЩЕЕ БОЛЬШИНСТВО ОРГАНИЗАЦИИ,<br>ПРЕДОСТАВЛЯЮЩИХ ПАРКОВОЧНЫЕ МЕСТА В АРЕНДУ [9,19].\\\\</b>n<br>\\\\x0c</p></body></html>"}
```


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
В случае ошибок или action=4 в  ```volume``` сгенерируется отчет о произошедшем
___
Парраметры:
+ ```size``` - обязательный параметр, длинна шингла для работы системы
+ ```action``` - обязательный параметр, действие, которое будет делать система
+ ```doc_path``` - путь/имя документа для обработки (документ должен лежать в ```volume``` в папке ```container_dir```)
+ ```doc_id``` - id документа для реиндексации
+ ```docs_id``` - список id документов для реиндексации
___
action_list:
+ 0 - получить статус документа (документ в обработке, или уже обработался - тогда вернется результат)
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

```bash
ACTION=0
DOC_ID=10005
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}&doc_id={DOC_ID}"
```
Для данного документа вернется ответ:
Либо он в обработке, либо уже обработался (тогда вернется результат обработки)
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
Для отслеживарния реиндексации всей коллекции документов предусмотрена возможность обращаться через action=0 с параметром doc_id=-1. В таком случае вернется состоянии обработки.
___
Получение списка стоп слов 
```bash
ACTION=4
curl "${BASE_URL}?size=&{SIZE}&action=${ACTION}"
```
Список стоп слов сгенерируется в ```volume``` в репорте.