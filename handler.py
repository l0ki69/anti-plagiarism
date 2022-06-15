import json
from json import JSONDecodeError
import os

from flask import Flask, request, make_response, jsonify
import subprocess
from Plahiarismhandler import Plahiarismhandler


app = Flask(__name__)


class Params:
    SIZE = "size"
    DOC_ID = "doc_id"
    DOCS_ID = "docs_id"


def check_base_param(request) -> bool:
    return request.args.get(Params.SIZE) == Params.SIZE.upper()


def return_result_json(result: str, status_code: int):
    return jsonify({"result": result, "status_code": status_code})


def return_error(error: str, status_code: int):
    return jsonify({"status_code": status_code, "error": error})


def get_args(request, key: str = 'base_value') -> list:
    args = request.args
    size = args.get(Params.SIZE, None)
    result = [None]
    if size is not None:
        if int(size) <= 0 or int(size) > 10:
            result = [None]
        else:
            result = [str(size)]

    if key != 'base_value':
        result.append(str(args.get(key, None)))

    return result


@app.route('/plagiarism/reindex/', methods=['GET'])
def reindex_handler():
    cmd = ["python3.8", "main.py", "reindex"]
    try:
        if not request.args.keys():
            return jsonify({"reindex": f"{request.base_url}?{Params.SIZE}={Params.SIZE.upper()}"
                                       f"&{Params.DOC_ID}={Params.DOC_ID.upper()}"})

        if check_base_param(request):
            return return_result_json("Enter parameters", 200)

        size, doc_id = get_args(request, Params.DOC_ID)

        if None in [size, doc_id]:
            return return_error(f"Parameters {request.args} uncorrect", 400)

        cmd.extend([str(size), str(doc_id)])

        subprocess.Popen(cmd, close_fds=True)

        return jsonify(f"document = {doc_id} processing started", 200)
    except Exception as e:
        return return_error(f'An error has occurred - "{e}"', 400)


@app.route('/plagiarism/reindex_list/', methods=['GET'])
def reindex_list_handler():
    cmd = ["python3.8", "main.py", "reindex_list"]
    try:
        if not request.args.keys():
            return jsonify({"reindex_list": f"{request.base_url}?{Params.SIZE}={Params.SIZE.upper()}"
                                            f"&{Params.DOCS_ID}={Params.DOC_ID.upper()};{Params.DOC_ID.upper()}"})

        if check_base_param(request):
            return jsonify("Enter parameters", 200)

        size, docs_id = get_args(request, Params.DOCS_ID)

        if None in [size, docs_id]:
            return return_error(f"Parameters {request.args} uncorrect", 400)

        cmd.extend([str(size)])

        list_docs = []
        for doc_id in docs_id.split(';'):
            list_docs.append(str(int(doc_id)))

        cmd.extend(list_docs)

        subprocess.Popen(cmd, close_fds=True)

        return jsonify(f"documents = {list_docs} processing started", 200)
    except Exception as e:
        return return_error(f'An error has occurred - "{e}"', 400)


@app.route('/plagiarism/reindex_all/', methods=['GET'])
def reindex_all_handler():
    cmd = ["python3.8", "main.py", "reindex_all"]
    try:
        if not request.args.keys():
            return jsonify({"reindex_all": f"{request.base_url}?{Params.SIZE}={Params.SIZE.upper()}"})

        if check_base_param(request):
            return jsonify("Enter parameters", 200)

        size = get_args(request)

        if None in size:
            return return_error(f"Parameters {request.args} uncorrect", 400)

        cmd.extend([str(size[0])])

        subprocess.Popen(cmd, close_fds=True)

        return return_result_json(f"reindex_all processing started", 200)
    except Exception as e:
        return return_error(f'An error has occurred - "{e}"', 400)


@app.route('/plagiarism/get_report/', methods=['GET'])
def get_report_handler():
    try:
        if not request.args.keys():
            return jsonify({"get_report": f"{request.base_url}?{Params.SIZE}={Params.SIZE.upper()}"
                                          f"&{Params.DOC_ID}={Params.DOC_ID.upper()}"})

        if check_base_param(request):
            return return_result_json("Enter parameters", 200)

        size, doc_id = get_args(request, Params.DOC_ID)

        if None in [size, doc_id]:
            return return_error(f"Parameters {request.args} uncorrect", 400)

        handler = Plahiarismhandler(int(size))
        result = handler.psql.get_result(doc_id=int(doc_id), size=size)
        if result is None:
            return return_error(f"No such document = {doc_id} exists with size = {size}", 400)
        result = result[0]

        if result['processing']:
            if result['doc_id'] != -1:
                try:
                    result['result_json'] = json.loads(result['result_json'])
                    return jsonify(result)
                except JSONDecodeError as js:
                    return jsonify({"error": f"JSONDecodeError - {js}, failed convert to json", "result": result})

            else:
                return return_result_json("reindex_all complete", 200)
        else:
            return return_result_json(f"doc = {doc_id} and size = {size} processing", 200)

    except Exception as e:
        return return_error(f'An error has occurred - "{e}"', 400)


@app.route('/plagiarism/get_stop_words/', methods=['GET'])
def get_stop_words_handler():
    cmd = ["python3.8", "main.py", "get_stop_words", "-1"]
    try:
        subprocess.Popen(cmd, close_fds=True)
        return return_result_json(f"get_stop_words completed", 200)
    except Exception as e:
        return return_error(f'An error has occurred - "{e}"', 400)


@app.route('/plagiarism/add_document/', methods=['GET'])
def add_document_handler_get():
    return jsonify({"add_document": f'|curl -F "file=@PATH_FILE;filename=FILENAME" "{request.base_url}?size=SIZE"|'})


@app.route('/plagiarism/add_document/', methods=['POST'])
def add_document_handler():
    cmd = ["python3.8", "main.py", "add_document"]
    if 'file' not in request.files:
        return return_error('File not found', 400)

    file = request.files['file']
    file_name = file.filename
    size = get_args(request)

    if None in size:
        return return_error(f"Parameters {request.args} uncorrect", 400)

    if not file_name:
        return return_error("File_name error", 400)

    file.save(f'{file_name}')
    handler = Plahiarismhandler(int(size[0]))
    doc_id = handler.add_document(file_name)
    os.remove(file_name)
    cmd.extend([str(size[0]), str(doc_id)])

    subprocess.Popen(cmd, close_fds=True)

    return jsonify({"doc_id": doc_id})


@app.route('/plagiarism', methods=['GET'])
def handler():
    methods = ["get_report", "add_document", "reindex", "reindex_list", "reindex_all", "get_stop_words"]
    methods_result = {method: f"{request.base_url}/{method}/" for method in methods}

    return jsonify(methods_result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
