import os
from container_dir.config import PSQL_USER, PSQL_PASSWORD, PSQL_HOST, \
                   PSQL_PORT, PSQL_DATABASE, PSQL_TABLE_SHINGLES, PSQL_TABLE_TEXT_PAGE, PSQL_TABLE_PROCESSING

import psycopg2
from psycopg2 import Error


class PSQL:
    def __init__(self, user=PSQL_USER,
                 password=PSQL_PASSWORD,
                 host=PSQL_HOST,
                 port=PSQL_PORT,
                 database=PSQL_DATABASE):
        try:
            self.connection = psycopg2.connect(user=user,
                                               password=password,
                                               host=host,
                                               port=port,
                                               database=database)

            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Error while working with PostgreSQL", error)

    def __del__(self):
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()

    def get_text_document(self, document_id: int):
        self.cursor.execute(f"SELECT page_num, page_text FROM {PSQL_TABLE_TEXT_PAGE} WHERE doc_id={document_id};")
        result = self.cursor.fetchall()
        result_js = [{'page_num': res[0], 'page_text': res[1]} for res in result]
        text = ""
        result_js = sorted(result_js, key=lambda hs: int(hs["page_num"]))
        for page in result_js:
            text += page['page_text']

        return text

    def get_shingles(self, shingles: list, shingle_size: int):
        if len(shingles) > 1:
            self.cursor.execute(f"SELECT id, ip_id, term, size, hash FROM {PSQL_TABLE_SHINGLES} WHERE hash IN {tuple(shingles)} and size = {shingle_size};")
        else:
            self.cursor.execute(f"SELECT id, ip_id, term, size, hash FROM {PSQL_TABLE_SHINGLES} WHERE hash = '{shingles[0]}' and size = {shingle_size};")
        result = self.cursor.fetchall()
        if result:
            result_js = [{'id': res[0], 'ip_id': res[1], 'term': res[2], 'size': res[3], 'hash': res[4]} for res in result]
            return result_js
        else:
            return []

    def remove_doc(self, document_id: int, size_shingle: int):
        self.cursor.execute(f"DELETE FROM {PSQL_TABLE_SHINGLES} WHERE ip_id = {document_id} and size={size_shingle};")
        self.connection.commit()

    def insert_row(self, row):
        self.cursor.execute(f"INSERT INTO {PSQL_TABLE_SHINGLES} (ip_id, term, times, size, hash) VALUES {tuple(row)};")
        self.connection.commit()

    def get_all_documents(self):
        self.cursor.execute(f"SELECT doc_id FROM {PSQL_TABLE_TEXT_PAGE};")
        result = self.cursor.fetchall()
        return [res[0] for res in result]

    def add_document(self, text: str) -> int:
        self.cursor.execute(f"SELECT nextval('in_pages_id_seq_doc');")
        doc_id = int(list(self.cursor.fetchall())[0][0])
        row = tuple([doc_id, 1, text])
        self.cursor.execute(f"INSERT INTO {PSQL_TABLE_TEXT_PAGE} (doc_id, page_num, page_text) VALUES {row};")
        self.connection.commit()
        return doc_id

    def get_result(self, doc_id: int, size: int):
        if doc_id == -2:
            return None
        self.cursor.execute(f"SELECT * FROM {PSQL_TABLE_PROCESSING} WHERE doc_id={doc_id} and size={size};")
        result = self.cursor.fetchall()
        if not result:
            return None
        result_js = [{'doc_id': res[0], 'result_json': res[1], 'size': res[2], 'processing': res[3], "html": res[4]} for res in result]
        return result_js

    def add_result(self, doc_id: str, result: str, size: int, processing: bool, html_text: str):
        self.cursor.execute(f"DELETE FROM {PSQL_TABLE_PROCESSING} WHERE doc_id = {doc_id} and size={size};")
        self.connection.commit()
        row = [int(doc_id), result, size, processing, html_text]
        self.cursor.execute(f"INSERT INTO {PSQL_TABLE_PROCESSING} (doc_id, result_json, size, processing, html_text) VALUES {tuple(row)};")
        self.connection.commit()
