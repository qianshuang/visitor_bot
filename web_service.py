# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import request
from gevent import pywsgi

from helper import *

import atexit

app = Flask(__name__)


@app.route('/trie_search', methods=['GET', 'POST'])
def trie_search():
    """
    input json:
    {
        "data": "xxxxxx",  # 用户query
        "size": 10         # 最大返回大小
    }

    return:
    {   'code': 0,
        'msg': 'success',
        'data': []
    }
    """
    resq_data = json.loads(request.get_data())
    data = resq_data["data"].strip()
    size = int(resq_data["size"]) if "size" in resq_data else default_size

    # 1. 原句trie
    trie_res = smart_hint(data)
    # 2. 标点最后1句trie
    if len(trie_res) == 0:
        trie_res = smart_hint(re.split(r'[,|.]', data)[-1])

    priorities_res = priorities
    ranked_trie_res = rank(list(set(trie_res) - set(priorities_res)))
    result = {'code': 0, 'msg': 'success', 'data': (priorities_res + ranked_trie_res)[:size]}
    return result


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    """
        {
            "data": "xxxxxx"  # 用户query
        }
    """
    resq_data = json.loads(request.get_data())
    data = resq_data["data"].strip()

    # 回写recent文件
    # global recents
    if data in recents:
        recents.remove(data)
    recents.insert(0, data)
    # write_lines(RECENT_FILE, recents)

    # 回写frequency文件
    frequency.setdefault(data, 0)
    frequency[data] = frequency[data] + 1
    # open_file(FREQUENCY_FILE, mode='w').write(json.dumps(frequency, ensure_ascii=False))

    result = {'code': 0, 'msg': 'success', 'data': data}
    return jsonify(result)


def exit_handler():
    print('Flask is exiting, starting writing resource files...')
    write_lines(RECENT_FILE, recents)
    open_file(FREQUENCY_FILE, mode='w').write(json.dumps(frequency, ensure_ascii=False))


atexit.register(exit_handler)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8088), app)
    server.serve_forever()
    # app.run(debug=False, threaded=True, host='0.0.0.0', port=8088)
