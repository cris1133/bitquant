import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cPickle as pickle
import requests
import json
import decimal
import time
global pulls

pulls = 0
global cycles
cycles = 0
#
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

def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass


def animate(i):
    global pulls
    global cycles
    orders = getOrderBook()
    transactions = getTransactions()
    ticker = getTicker()
    bids = np.array([[float(price[0]), float(price[1])] for price in orders['bids']])
    asks = np.array([[float(price[0]), float(price[1])] for price in orders['asks']])

    x_bids=bids[:20,0]
    y_bids=bids[:20,1].cumsum()
    x_asks=asks[:20,0]
    y_asks=asks[:20,1].cumsum()

    price = float(ticker[u'last'])

    line.set_data(x_bids, y_bids)  # update the data
    line2.set_data(x_asks,y_asks)
    price_line.set_xdata(price)
    

    cycles += 1
    if cycles > 40:
        pulls = 0
    if pulls > 400:
        time.sleep(600)

    return line,line2,price_line

def init():
    line.set_ydata(np.ma.array(np.arange(20), mask=True))
    line2.set_ydata(np.ma.array(np.arange(20), mask=True))
    price_line.set_xdata(0.0)
    return line,line2,price_line

fig, ax = plt.subplots()
ax.set_ylim(0,500)
ax.set_xlim(388,398)

orders = getOrderBook()
transactions = getTransactions()
ticker = getTicker()

bids = np.array([[float(price[0]), float(price[1])] for price in orders['bids']])
asks = np.array([[float(price[0]), float(price[1])] for price in orders['asks']])

x_bids=bids[:20,0]
y_bids=bids[:20,1].cumsum()
x_asks=asks[:20,0]
y_asks=asks[:20,1].cumsum()

price = float(ticker[u'last'])

#x = np.arange(0, 2*np.pi, 0.01)        # x-array
line,line2,price_line = ax.plot(x_bids, y_bids)[0],ax.plot(x_asks, y_asks)[0], ax.axvline(price,ls='--')

#Init only required for blitting to give a clean slate.


ani = animation.FuncAnimation(fig, animate, init_func=init,
    interval=15000, blit=True)


plt.show()