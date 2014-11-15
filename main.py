import requests
import json
import decimal
import time
import numpy
global pulls
pulls = 0
global prevorders
prevorders = []
## Data fetching helper functions
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


## Paper-trade simulation system
class papertrade(object):
	"""All transaction amounts are in BTC"""
	def __init__(self):
		self.buys = []
		self.sells = []
		## BTC in Satoshi
		self.btc = 0
		self.usd = 1000
	def buy(self, amount):
		price = float(getTicker()['ask'])
		if self.usd < (amount * price):
			return False
		self.buys.append({"amount":amount, "price":price})
		self.usd = self.usd - (amount * price)
		self.btc = self.btc + (amount*100000000)
		return price
	def sell(self, amount):
		price = float(getTicker()['bid'])
		if self.btc < (amount*100000000):
			return False
		self.sells.append({"amount":amount, "price":price})
		self.btc = self.btc - (amount*100000000)
		self.usd = self.usd + (amount * price)
		return price

def findPeak(data):
	data = data[:20]
	last = 0
	lastV = 0
	for item in range(len(data)-1):
		diff = float(data[item+1][1]) - float(data[item][1])
		if diff > last:
			last = diff
			lastV = item

## Quant helper functions
def getBias(orders):
	bids = orders["bids"]
	asks = orders["asks"]
	bids = bids[:findPeak(bids)]
	asks = asks[:findPeak(asks)]
	bV = [float(n[1]) for n in bids]
	aV = [float(n[1]) for n in asks]
	bRatio = (float(bids[-1][0]) - float(bids[0][0])) / float(bids[-1][1]) / sum(bV)
	aRatio = (float(asks[-1][0]) - float(asks[0][0])) / float(asks[-1][1]) / sum(aV)
	if abs(bRatio) > aRatio:
		return "ask"
	else:
		return "bid"

## Testing stuff here
def test():
	## 0 = buy, 1 = sell
	mode = 0
	trade = papertrade()
	boughtAt = 0
	cycles = 0
	global pulls
	while 1==1:
		orders = getOrderBook()
		global prevorders
		prevorders.append(orders)
		transactions = getTransactions()
		## Non trivial stuff starts here
		if mode == 0:
			bias = getBias(orders)
			if bias == "bid":
				boughtAt = trade.buy(0.1)
				mode = 1
				print "BOUGHT 0.1BTC @ "+ str(boughtAt)
				print trade.btc, trade.usd
		else:
			if getBias(orders) == "ask":
				trade.sell(0.1)
				print "SOLD 0.1BTC"
				print trade.btc, trade.usd
				mode = 0
			else:
				print "HOLDING BTC"
		cycles += 1
		if cycles > 40:
			pulls = 0
		if pulls > 400:
			time.sleep(600)
		time.sleep(15)