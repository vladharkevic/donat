
import requests
import time
import json
import os
from config import MONOBANK_TOKEN

TXN_LOG = 'used_txns.json'

def get_transactions():
    url = 'https://api.monobank.ua/personal/statement/0/' + str(int(time.time()))
    headers = {'X-Token': MONOBANK_TOKEN}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def load_used_txns():
    if not os.path.exists(TXN_LOG):
        with open(TXN_LOG, 'w') as f:
            json.dump([], f)
    with open(TXN_LOG, 'r') as f:
        return json.load(f)

def save_used_txn(txn_id):
    used = load_used_txns()
    used.append(txn_id)
    with open(TXN_LOG, 'w') as f:
        json.dump(used, f)

def find_payment(amount_uah):
    transactions = get_transactions()
    used = load_used_txns()
    now = int(time.time())

    for txn in transactions[::-1]:
        if txn['operationAmount'] < 0:
            txn_amount = abs(txn['operationAmount']) / 100
            txn_time = txn['time']
            txn_id = txn['id']

            if txn_id in used:
                continue

            if abs(txn_amount - amount_uah) < 0.1 and now - txn_time < 300:
                save_used_txn(txn_id)
                return True
    return False
