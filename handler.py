import json

from flask import Flask, request, make_response
from subprocess import Popen, PIPE

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_handler():
    result = {
        'statusCode': 200,
        'body': 'message_complete'
    }
    try:
        args = request.args

        size = int(args.get('size', -1))
        action = int(args.get('action', -1))

        if -1 in [size, action] or action not in [0, 1, 2, 3, 4]:
            result['statusCode'] = 400
            result['body'] = 'action or size not defined'

        if result['statusCode'] == 200:
            cmd = ["python3.8", "main.py", str(size), str(action)]
            if action == 0:
                cmd.append(str(args.get('doc_path', "-1")))
            elif action == 1:
                cmd.append(str(args.get('doc_id', "-1")))
            elif action == 2:
                temp_arg = args.get('docs_id', "")
                for temp in temp_arg.split(","):
                    cmd.append(str(int(temp)))

            # Запускает main.py
            process = Popen(cmd, stdout=PIPE)
            outs, errs = process.communicate()
            outs = str(outs.decode("utf-8"))
            outs = outs.replace("\n", "<br>")
            result['body'] = f'outs - {outs}<br>errs - {errs}'
            rc = process.wait()
            assert rc == 0

    except Exception as e:
        outs = str(e)
        result['body'] = f"error - '{outs}'"
        result['statusCode'] = 502

    if result['statusCode'] != 200:
        result['statusCode'] = 502

    answer = make_response(json.dumps(result['body']), result['statusCode'])
    return answer


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
