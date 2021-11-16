import random

import MySQLdb.cursors
from tqdm import tqdm

_config = {
    'db_host': 'localhost',
    'db_port': 3306,
    'db_username': 'scouty',
    'db_password': 'scouty',
    'db_database': 'scoutea',
}

_f = open('./data/japan_location.txt')
_japan_location = list(set(_f.read().split()))
_japan_location = [[l, '日本'] for l in _japan_location]
_f = open('./data/china_location.txt')
_china_location = list(set(_f.read().split()))
_china_location = [[l, '中国'] for l in _china_location]
_f = open('./data/india_location.txt')
_india_location = list(set(_f.read().split()))
_india_location = [[l, 'インド'] for l in _india_location]
LOCATIONS = _japan_location + _china_location + _india_location

_f = open('./data/sentence.txt')
SENTENCES = _f.read().split()

_f = open('./data/kana.txt')
KANA_LIST = _f.read().split()


def config(key):
    if key in _config:
        return _config[key]
    else:
        raise "config value of %s undefined" % key


def db():
    _db = MySQLdb.connect(**{
        'host': config('db_host'),
        'port': config('db_port'),
        'user': config('db_username'),
        'passwd': config('db_password'),
        'db': config('db_database'),
        'charset': 'utf8mb4',
        'cursorclass': MySQLdb.cursors.DictCursor,
        'autocommit': True,
    })
    cur = _db.cursor()
    cur.execute("SET SESSION sql_mode='TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY'")
    cur.execute('SET NAMES utf8mb4')
    return _db


def insert_locations():
    print('insert locations')
    random.shuffle(LOCATIONS)

    cur = db().cursor()
    cur.execute('INSERT INTO locations (name) VALUES ("日本"), ("中国"), ("インド")')
    for l in tqdm(LOCATIONS):
        location = l[0]
        country = l[1]

        cur.execute('INSERT INTO locations (name) VALUES ("{}")'.format(location))
        cur.execute('SELECT id FROM locations WHERE name = "{}"'.format(location))
        location_id = cur.fetchone()['id']
        cur.execute('SELECT id FROM locations WHERE name = "{}"'.format(country))
        country_id = cur.fetchone()['id']
        cur.execute('INSERT INTO location_relations (location_from_id, location_to_id) VALUES ({}, {})'.format(location_id, country_id))


def insert_teas():
    print('insert teas')
    cur = db().cursor()
    for i in tqdm(range(5000)):
        query = 'INSERT INTO teas (name, location, description) VALUES '
        for _ in range(100):
            name = ''.join(random.sample(KANA_LIST, 6)) + '茶'
            location = random.sample(LOCATIONS, 1)[0][0]
            description = ''.join(random.sample(SENTENCES, 10))
            query += '("{}", "{}", "{}"),'.format(name, location, description)
        cur.execute(query[0:-1])


def insert():
    insert_locations()
    insert_teas()


if __name__ == "__main__":
    insert()
