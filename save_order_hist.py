import requests
import json
import decimal
import time
import numpy
import cPickle as pickle
global pulls
#
pulls = 0

def getOrderBook():
    global pulls
    pulls = pulls + 2
    return json.loads(requests.get("https://www.bitstamp.net/api/order_book/").content)
def getTransactions():
    global pulls
    pulls = pulls + 1
    return json.loads(requests.get("https://www.bitstamp.net/api/transactions/").content)
def getTicker():
    global pulls
    pulls = pulls + 1
    return json.loads(requests.get("https://www.bitstamp.net/api/ticker/").content)

def save_orders():
    global pulls
    cycles = 0
    while 1==1:
        orders = getOrderBook()
        transactions = getTransactions()
        ticker = getTicker()
        save_orders = {'time' : orders['timestamp'], 'bids' : orders['bids'], 'asks' : orders['asks'], 'transactions': transactions, 'ticker': ticker}
        pickle.dump(save_orders, open("output.p", "ab"))
        print("saved orders at time {0}".format(orders['timestamp']))
        
        cycles += 1
        if cycles > 40:
            pulls = 0
        if pulls > 400:
            time.sleep(600)
        time.sleep(30)