import requests
import json
import decimal
import time
global transactions
pulls = 0

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
		self.btc = 100000000
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


## Quant helper functions
def compareVolume(orders):
	buys = [float(n[1]) for n in orders["bids"]]
	sells = [float(n[1]) for n in orders["asks"]]
	if sum(buys) > sum(sells):
		return "buys"
	else:
		return "sells"

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
		transactions = getTransactions()
		bias = compareVolume(orders)
		if mode == 0:
			if bias == "buys" and trade.btc > (100000000*0.1):
				boughtAt = trade.buy(0.1)
				mode = 1
		else:
			if float(getTicker()['bid']) > boughtAt:
				trade.sell(0.1)
				mode = 0
		print trade.btc, trade.usd, pulls
		cycles += 1
		if cycles > 40:
			pulls = 0
		if pulls > 400:
			time.sleep(600)
		time.sleep(15)