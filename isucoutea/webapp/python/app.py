import math
import pathlib

import MySQLdb.cursors
from flask import Flask, redirect, render_template, request

static_folder = pathlib.Path(__file__).resolve().parent / 'css'
app = Flask(__name__, static_folder=str(static_folder), static_url_path='')

app.secret_key = 'drink_tea'

_config = {
    'db_host': 'localhost',
    'db_port': 3306,
    'db_username': 'scouty',
    'db_password': 'scouty',
    'db_database': 'scoutea',
}

TEAS_PER_PAGE = 6


def config(key):
    if key in _config:
        return _config[key]
    else:
        raise "config value of %s undefined" % key


def db():
    if hasattr(request, 'db'):
        return request.db

    request.db = MySQLdb.connect(**{
        'host': config('db_host'),
        'port': config('db_port'),
        'user': config('db_username'),
        'passwd': config('db_password'),
        'db': config('db_database'),
        'charset': 'utf8mb4',
        'cursorclass': MySQLdb.cursors.DictCursor,
        'autocommit': True,
    })
    cur = request.db.cursor()
    cur.execute("SET SESSION sql_mode='TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY'")
    cur.execute('SET NAMES utf8mb4')
    return request.db


def get_country(tea):
    cur = db().cursor()
    cur.execute('SELECT id FROM locations WHERE name = "{}"'.format(tea['location']))
    location_id = cur.fetchone()['id']
    cur.execute('SELECT location_to_id FROM location_relations WHERE location_from_id = {}'.format(location_id))
    country_id = cur.fetchone()['location_to_id']
    cur.execute('SELECT name FROM locations WHERE id = {}'.format(country_id))
    return cur.fetchone()['name']


@app.route('/')
def index():
    page = max(int(request.args.get('page', 1)), 1)
    query = request.args.get('query', '')
    offset = (page - 1) * TEAS_PER_PAGE

    cur = db().cursor()
    cur.execute('SELECT * FROM teas ORDER BY id DESC')
    teas = cur.fetchall()

    teas_match = []
    for tea in teas:
        if query == '':
            teas_match.append(tea)
            continue

        tea['country'] = get_country(tea)
        if query == tea['name'] or query == tea['location'] or query == tea['country']:
            teas_match.append(tea)

    teas_display = []
    for i, tea in enumerate(teas_match):
        if offset <= i and i < offset + TEAS_PER_PAGE:
            tea['country'] = get_country(tea)
            tea['description'] = tea['description'][:100] + '...' if len(tea['description']) > 100 else tea['description']
            teas_display.append(tea)

    first_page = 1
    current_page = page
    last_page = math.ceil(len(teas_match) / 6)

    return render_template('index.html',
                           teas=teas_display,
                           query=query,
                           url_query='&query={}'.format(query) if query else '',
                           first_page=first_page,
                           current_page=current_page,
                           last_page=last_page)


@app.route('/', methods=['POST'])
def create():
    name = request.form['name']
    location = request.form['location']
    description = request.form['description']

    cur = db().cursor()
    location_exist = cur.execute('SELECT 1 FROM locations WHERE name = "{}"'.format(location))
    if location_exist:
        cur.execute('INSERT INTO teas (name, location, description) VALUES ("{}", "{}", "{}")'.format(name, location, description))
    return redirect('/')


@app.route('/new')
def new():
    return render_template('new.html')


@app.route('/initialize')
def initialize():
    cur = db().cursor()
    cur.execute('DELETE FROM teas WHERE id > 500000')
    cur.execute('DELETE FROM locations WHERE id > 2397')
    cur.execute('DELETE FROM location_relations WHERE id > 2394')
    return redirect('/')


if __name__ == "__main__":
    app.run()
