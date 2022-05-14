Anti-plagiarism
===========
---

System for detecting borrowed text fragments in an indexed collection of documents


## Installation

___

1) Python 3.8 [install](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
2) ```python3.8 -m pip install -r requirements.txt```
3) ```bash start.sh```

## Note

Система проверяет на процент уникальности два текста, которые находятся в файлах ```text_1.in``` и ```text_2.in```.
Результат выводится в консоль и файл ```output.out```.

Для запуска без sh скипрта - ```python3.8 main.py "text_1.in" "text_2.in"```