from typing import List, Dict
import os
import sys
import json
from dotenv import load_dotenv

from Plahiarismhandler import Plahiarismhandler


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    args = sys.argv
    action = args[1]

    handler = Plahiarismhandler()
    if action in ["index_document", '1']:
        doc_id = args[2]
        result = handler.documents_indexing([int(doc_id)])
    elif action in ["index_documents", '2']:
        docs_id = []
        for arg in range(2, len(args)):
            docs_id.append(int(args[arg]))
            result = handler.documents_indexing(docs_id)
    elif action in ["index_all_documents", '3']:
        result = handler.all_documents_indexing()
    elif action in ["get_stop_words", '4']:
        result = handler.get_stop_words()
    else:
        result = {'result': "not found action"}

    with open('output.json', 'w') as out:
        json.dump(result, out, indent=2, ensure_ascii=False)