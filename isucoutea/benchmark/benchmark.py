import time

import requests

ROOT_URL = 'http://app'
TIMEOUT_SEC = 20

QUERIES = [
    {'method': 'GET', 'path': '/', 'asserts': ['<h4 class="my-0 font-weight-normal text-center">ヌジュギュセピウ茶</h4>', '<li><strong>生産地:</strong> 和束町</li>', '<li><strong>生産国:</strong> 日本</li>', '<li><strong>説明:</strong> 回転するドラムに茶葉を入れ熱風を通して茶葉を乾燥するため、撚れておらず、丸いぐりっとした形状に仕上がったお茶です。ごく少量生産される烏龍茶の一種。味わいとしては、甘みを含んだ独特の芳香をもっており、お...</li>', 'ヒョシレマペユ茶', 'ゴーパールガンジ'], 'not_asserts': ['トハスゴユラ茶']},
    {'method': 'GET', 'path': '/?page=80000', 'asserts': ['キョミュパペベラ茶', 'マチリーパトナム', 'ガドツケヂヨ茶', '厚沢部町'], 'not_asserts': ['ジャリュチョビニョチュ茶']},
    {'method': 'POST', 'path': '/', 'data': {'name': '新しいお茶', 'location': '標茶町', 'description': '採れたてだよ。'}, 'asserts': ['新しいお茶', '標茶町', '採れたてだよ。', 'ユミワキャモン茶'], 'not_asserts': ['ヒョシレマペユ茶']},
    {'method': 'GET', 'path': '/?page=25&query=平塚市', 'asserts': ['スサメリジュチョ茶', 'ベリュフタデミャ茶', 'スニクホケモ茶', 'ゴハヒュプギイ茶', 'タゲチュダミア茶', 'リャハボキャヒャギョ茶'], 'not_asserts': ['インド', '中国']},
    {'method': 'GET', 'path': '/?page=858&query=日本', 'asserts': ['メパバビムフ茶', 'ツブムショジュケ茶', 'ザポヤリョショグ茶', 'ヅホタメゼヤ茶', 'ヂレヒャベチフ茶', 'ヅヘベニュジャド茶'], 'not_asserts': ['インド', '中国']},
    {'method': 'GET', 'path': '/', 'asserts': ['新しいお茶', '標茶町', '採れたてだよ。', 'ユミワキャモン茶'], 'not_asserts': ['ヒョシレマペユ茶']},
    {'method': 'POST', 'path': '/', 'data': {'name': '更に新しいお茶', 'location': 'デリー', 'description': '更に採れたてだよ。'}, 'asserts': ['更に新しいお茶', 'デリー', '更に採れたてだよ。', 'メガンヤリバ茶'], 'not_asserts': ['ユミワキャモン茶']},
    {'method': 'GET', 'path': '/?query=ミャメビエコフ茶', 'asserts': ['<h4 class="my-0 font-weight-normal text-center">ミャメビエコフ茶</h4>', '白老町', '日本', '渋みと甘みのバランスを味わってください。'], 'not_asserts': ['インド', '中国']},
    {'method': 'GET', 'path': '/?query=存在しないお茶', 'asserts': ['存在しないお茶'], 'not_asserts': ['<h4 class="my-0 font-weight-normal text-center">存在しないお茶</h4>', '日本', 'インド', '中国']},
    {'method': 'GET', 'path': '/', 'asserts': ['更に新しいお茶', 'デリー', '更に採れたてだよ。', 'メガンヤリバ茶'], 'not_asserts': ['ユミワキャモン茶']},
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
            content = response.content.decode()
            for condition in query['asserts']:
                assert condition in content, f'{condition} not in response:\n{content}'
            for condition in query['not_asserts']:
                assert condition not in content, f'{condition} in response:\n{content}'
        elif query['method'] == 'POST':
            response = requests.post(
                ROOT_URL + query['path'],
                data=query['data'],
                timeout=TIMEOUT_SEC
            )
            response.raise_for_status()
            content = response.content.decode()
            for condition in query['asserts']:
                assert condition in content, f'{condition} not in response:\n{content}'
            for condition in query['not_asserts']:
                assert condition not in content, f'{condition} in response:\n{content}'
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
