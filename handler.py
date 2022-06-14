import json

from flask import Flask, request, make_response
import subprocess
from Plahiarismhandler import Plahiarismhandler


app = Flask(__name__)


def return_result(message: str, status_code: int):
    return make_response(json.dumps({"body": message}), status_code)


@app.route('/', methods=['GET'])
def get_handler():
    cmd = ["python3.8", "main.py"]
    try:
        args = request.args
        size = int(args.get('size', -1))
        action = int(args.get('action', -1))

        if -1 in [size, action] or action not in [0, 1, 2, 3, 4]:
            return return_result("size or action error", 400)

        cmd.extend([str(size), str(action)])
        if action == 0:
            handler = Plahiarismhandler(size)
            result = handler.psql.get_result(doc_id=int(args.get('doc_id', -2)), size=size)
            if result is None:
                return return_result("doc_id error", 400)
            result = result[0]

            if result['processing']:
                return return_result(result['result_json'], 200)
            else:
                return return_result("doc processing", 200)

        elif action == 1:
            cmd.append(str(args.get('doc_id', "-1")))
        elif action == 2:
            temp_arg = args.get('docs_id', "")
            for temp in temp_arg.split(","):
                cmd.append(str(int(temp)))

        subprocess.Popen(cmd, close_fds=True)

    except Exception as e:
        return return_result(f"error - {e}", 400)

    return return_result("processing started", 200)


@app.route('/', methods=['POST'])
def post_handler():
    cmd = ["python3.8", "main.py"]
    if 'file' not in request.files:
        return return_result('file not found', 400)

    file = request.files['file']
    file_name = file.filename
    args = request.args

    if not file_name:
        return return_result("file_name error", 400)
    if 'size' not in args:
        return return_result("shingle size not found", 400)
    size = int(args['size'])

    if size <= 0:
        return return_result("size uncorrected", 400)

    file.save(f'{file_name}')
    handler = Plahiarismhandler(size)
    doc_id = handler.add_document(file_name)
    cmd.extend([str(size), str(1), str(doc_id)])
    subprocess.Popen(cmd, close_fds=True)

    return return_result(message=json.dumps({"doc_id": doc_id}), status_code=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
