FROM python:3.8.0

RUN apt-get -yqq update
RUN git clone https://github.com/l0ki69/anti-plagiarism.git
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /anti-plagiarism
RUN pip install virtualenv==20.14.1
#RUN python3.8 -m venv env
#RUN source env/bin/activate
RUN pip install -r requirements.txt
RUN python3.8 -m spacy download ru_core_news_md
