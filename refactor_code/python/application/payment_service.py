"""
モックの外部APIを叩く
"""
import requests

CARD_PAYMENT_API = 'http://paymentmock/api/card'
POYJP_PAYMENT_API = 'http://paymentmock/api/poyjp'
BANK_PAYMENT_API = 'http://paymentmock/api/bank'


def card_payment(card_number, price):
    res = requests.post(CARD_PAYMENT_API, json={
        'card_number': card_number,
        'price': price
    })
    return res.json()['success']


def poyjp_payment(account_number, price):
    res = requests.post(POYJP_PAYMENT_API, json={
        'account_number': account_number,
        'price': price
    })
    return res.json()['success']


def bank_payment(branch_number, account_number, price):
    res = requests.post(BANK_PAYMENT_API, json={
        'branch_number': branch_number,
        'account_number': account_number,
        'price': price
    })
    return res.json()['success']
