import datetime
import json
from hashlib import sha256

from peewee import *
from flask_login import UserMixin

from settings import DATABASE


class User(UserMixin, Model):
    name = CharField()
    password = CharField()

    class Meta:
        database = DATABASE

    def __str__(self):
        return '{}:{}'.format(self.id, self.name)

    @classmethod
    def create(cls, **query):
        query['password'] = cls.get_hashed_password(query['password'])
        return super().create(**query)

    def set_password(self, raw_password):
        self.password = self.get_hashed_password(raw_password)
        self.save()

    @classmethod
    def get_hashed_password(cls, raw_password):
        return sha256(raw_password.encode('utf-8')).hexdigest()


class Tea(Model):
    name = CharField()
    price = IntegerField()
    description = TextField()
    stock_amount = IntegerField()
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

    @property
    def display_updated_at(self):
        return datetime.datetime.strftime(self.updated_at, '%Y-%m-%d')


class Cart(Model):
    user = ForeignKeyField(User, backref='mycart')
    teas_data = TextField(default=json.dumps({}))

    class Meta:
        database = DATABASE

    @classmethod
    def create(cls, **query):
        if 'teas_dict' in query:
            query['teas_data'] = cls._teas_dict_to_json(query['teas_dict'])
            del query['teas_dict']
        return super().create(**query)

    @classmethod
    def _teas_dict_to_json(cls, teas_dict):
        return json.dumps(teas_dict)

    @classmethod
    def _teas_json_to_dict(cls, teas_json):
        return json.loads(teas_json)

    @property
    def teas_dict(self):
        return self._teas_json_to_dict(self.teas_data)

    def update_teas_data(self, teas_dict):
        self.teas_data = self._teas_dict_to_json(teas_dict)
        self.save()


class Order(Model):
    user = ForeignKeyField(User, backref='mycart')
    teas_data = TextField(default=json.dumps({}))  # cart.teas_dataのスナップショット
    payment_type = TextField(default='card')
    payment_info = TextField(null=True)  # カード番号とか
    status = IntegerField(default=0)  # 0 未払い, 1 引き落とし済み
    total_price = IntegerField()
    bought_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

    def __str__(self):
        return '{}: user:{}, pay:{}, price:{}'.format(
            self.id,
            self.user,
            self.payment_type,
            self.total_price
        )

    @classmethod
    def create(cls, **query):
        if 'teas_dict' in query:
            query['teas_data'] = cls._teas_dict_to_json(query['teas_dict'])
            del query['teas_dict']
        return super().create(**query)

    @classmethod
    def _teas_dict_to_json(cls, teas_dict):
        return json.dumps(teas_dict)

    @classmethod
    def _teas_json_to_dict(cls, teas_json):
        return json.loads(teas_json)

    @property
    def teas_dict(self):
        return self._teas_json_to_dict(self.teas_data)
