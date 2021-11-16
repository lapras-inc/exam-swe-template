import csv
import datetime

from pprint import pprint
from bottle import get, post, request, response, run, template, redirect

HISTORY_FILE = './history.csv'


def _write_history(*args):
    with open(HISTORY_FILE, 'a') as f:
        writer = csv.writer(f)
        data_list = [datetime.datetime.now()] + list(args)
        writer.writerow(data_list)


@get('/api/card')
@post('/api/card')
def card_payment():
    req = request.json
    pprint(req)
    _write_history('card', req['card_number'], req['price'])
    return {'success': True}


@get('/api/poyjp')
@post('/api/poyjp')
def card_payment():
    req = request.json
    pprint(req)
    _write_history('poyjp', req['account_number'], req['price'])
    return {'success': True}


@get('/api/bank')
@post('/api/bank')
def card_payment():
    req = request.json
    pprint(req)
    _write_history('bank', req['branch_number'], req['account_number'], req['price'])
    return {'success': True}


if __name__ == '__main__':
    run(host='0.0.0.0', port=80, reloader=True, debug=True)
