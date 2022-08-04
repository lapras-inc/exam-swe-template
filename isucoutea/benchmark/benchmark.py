import time

import requests

ROOT_URL = 'http://app'
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
    start = time.perf_counter()
    timeout = False
    try:
        if query['method'] == 'GET':
            response = requests.get(
                ROOT_URL + query['path'],
                timeout=TIMEOUT_SEC
            )
            response.raise_for_status()
        elif query['method'] == 'POST':
            response = requests.post(
                ROOT_URL + query['path'],
                data=query['data'],
                timeout=TIMEOUT_SEC
            )
            response.raise_for_status()
        end = time.perf_counter()
        process_time = end - start

    except requests.exceptions.ReadTimeout:
        timeout = True
        end = time.perf_counter()
        process_time = end - start

    except Exception as e:
        print('Error: ', query['method'], query['path'])
        raise e

    timeout_str = '(timeout)' if timeout else ''
    print('Request: ', query['method'], query['path'], process_time, 'sec', timeout_str)


def benchmark():
    start = time.perf_counter()

    for query in QUERIES:
        request(query)
    end = time.perf_counter()
    process_time = end - start

    print('Result:', process_time, 'sec')


def initialize():
    response = requests.get(ROOT_URL + '/initialize')
    response.raise_for_status()


if __name__ == "__main__":
    try:
        print('初期化処理を実施します...')
        initialize()
    except Exception as e:
        print(e)
        print('初期化処理に失敗しました...')
        exit(1)

    try:
        print('ベンチマークを実行します...')
        benchmark()
    except Exception as e:
        print(e)
        print('ベンチマーク実行に失敗しました...')
        exit(1)
