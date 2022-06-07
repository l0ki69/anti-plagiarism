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
        if action in ["add_document", '0']:
            doc_name = args[3]
            doc_id = handler.add_document(document_path=f'container_dir/{doc_name}')
            result = handler.documents_indexing([int(doc_id)])

        elif action in ["index_document", '1']:
            doc_id = args[3]
            result = handler.documents_indexing([int(doc_id)])
        elif action in ["index_documents", '2']:
            docs_id = []
            for arg in range(3, len(args)):
                docs_id.append(int(args[arg]))
                result = handler.documents_indexing(docs_id)
        elif action in ["index_all_documents", '3']:
            result = handler.all_documents_indexing()
        elif action in ["get_stop_words", '4']:
            result = handler.get_stop_words()
        else:
            result = [{"report": {"doc_id": "error", 'result': "not found action"}, "html": ""}]

        current_path = os.getcwd()

        if not os.path.exists(f"{current_path}/container_dir/reports_dir"):
            os.mkdir(f"{current_path}/container_dir/reports_dir")

        for ind, res in enumerate(result):
            html_path = f"{current_path}/container_dir/reports_dir/doc_{str(res['report'].get('document_id', ind))}.html"

            with open(html_path, 'w+') as h:
                h.write(res['html'])

            with open(f"{current_path}/container_dir/reports_dir/doc_{res['report'].get('document_id', ind)}.json", 'w+') as out:
                json.dump(result, out, indent=2, ensure_ascii=False)

        print('"status_code": 200, "body": "message_complete"')
    except Exception as e:
        print(f'"status_code": 400, "body": "{str(e)}"')