from peewee import Model

import models
from settings import DATABASE


def _find_models():
    model_list = []
    for name in dir(models):
        try:
            attr = getattr(models, name)
            if issubclass(attr, Model) and attr != Model:
                model_list.append(getattr(models, name))
        except:
            continue
    return model_list


def _insert_data():
    user_cls = models.User
    user_cls.create(name='testuser', password='testuser')
    tea_cls = models.Tea
    for i in range(20):
        tea_cls.create(
            name='tea_{}'.format(i),
            price=(10 + i % 3 * 10),
            stock_amount=(100 + i % 5 * 100),
            description='description of {}'.format(i),
        )


def init_db():
    DATABASE.connect()
    model_list = _find_models()
    print('target_models', model_list)
    print('#### drop tables')
    DATABASE.drop_tables(_find_models())
    print('#### crate tables')
    DATABASE.create_tables(_find_models(), safe=True)
    print('#### insert data')
    _insert_data()
