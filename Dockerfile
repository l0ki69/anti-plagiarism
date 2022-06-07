FROM python:3.8.0

RUN apt-get -yqq update
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /anti-plagiarism
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3.8 -m spacy download ru_core_news_md

RUN apt-get install -yqq antiword
RUN pip install Flask==2.0.2 requests==2.25.1
COPY *.py /anti-plagiarism/
COPY *.json /anti-plagiarism/
COPY handler.py handler.py
ENTRYPOINT ["python"]
CMD ["handler.py"]