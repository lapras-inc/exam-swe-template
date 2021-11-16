import time

import requests

ROOT_URL = 'http://localhost'
TIMEOUT_SEC = 20

QUERIES = [
    {'method': 'GET', 'path': '/'},
    {'method': 'GET', 'path': '/?page=80000'},
    {'method': 'POST', 'path': '/', 'data': {'name': '新しいお茶', 'location': '標茶町', 'description': '採れたてだよ。'}},
    {'method': 'GET', 'path': '/?page=25&query=平塚市'},
    {'method': 'GET', 'path': '/?page=858&query=日本'},
    {'method': 'GET', 'path': '/'},
    {'method': 'POST', 'path': '/', 'data': {'name': '更に新しいお茶', 'location': 'デリー', 'description': '更に採れたてだよ。'}},
    {'method': 'GET', 'path': '/?query=ミャメビエコフ茶'},
    {'method': 'GET', 'path': '/?query=存在しないお茶'},
    {'method': 'GET', 'path': '/'},
]


def request(query):
    try:
        if query['method'] == 'GET':
            requests.get(ROOT_URL + query['path'], timeout=TIMEOUT_SEC)
        elif query['method'] == 'POST':
            requests.post(ROOT_URL + query['path'], data=query['data'], timeout=TIMEOUT_SEC)
    except requests.exceptions.ReadTimeout:
        print('Timeout: ', query['method'], query['path'])


def benchmark():
    start = time.time()
    for query in QUERIES:
        request(query)
    process_time = time.time() - start

    print('Result:', process_time, 'sec')


def initialize():
    requests.get(ROOT_URL + '/initialize')


if __name__ == "__main__":
    initialize()
    benchmark()
