import sys
import json
import os
from Plahiarismhandler import Plahiarismhandler


if __name__ == '__main__':
    try:
        args = sys.argv
        shingle_size = int(args[1])
        action = args[2]
        handler = Plahiarismhandler(shingle_size)

        if action in ["index_document", '1']:
            doc_id = args[3]
            handler.psql.add_result(doc_id, "", shingle_size, False)
            result = handler.documents_indexing([int(doc_id)])
        elif action in ["index_documents", '2']:
            docs_id = []
            for arg in range(3, len(args)):
                handler.psql.add_result(int(args[arg]), "", shingle_size, False)
                docs_id.append(int(args[arg]))
                result = handler.documents_indexing(docs_id)
        elif action in ["index_all_documents", '3']:
            handler.psql.add_result(-1, "", shingle_size, False)
            result = handler.all_documents_indexing()
            handler.psql.add_result(-1, "", shingle_size, True)
        elif action in ["get_stop_words", '4']:
            result = handler.get_stop_words()
        else:
            result = [{"report": {"document_id": "error", 'result': "not found action"}, "html": ""}]

        current_path = os.getcwd()

        if result[0]['report']['document_id'] in ['stop_words', 'error']:
            with open(f'{current_path}/container_dir/report.json', 'w+') as f:
                f.write(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for ind, res in enumerate(result):
                handler.psql.add_result(doc_id=res['report'].get('document_id'),
                                        result=json.dumps(res, ensure_ascii=False),
                                        size=shingle_size,
                                        processing=True)

    except Exception as e:
        result = [{"report": {"doc_id": "error", 'result': f"error - {str(e)}"}, "html": ""}]
        with open(f'{os.getcwd()}/container_dir/report.json', 'w+') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))