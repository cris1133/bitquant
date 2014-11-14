import requests
import json
import decimal
from chain_bitcoin import Chain
chain = Chain(api_key_id='a62f58cb4594a5f284c7adb750e0f133')


def getOrderBook():
	return json.loads(requests.get("https://www.bitstamp.net/api/order_book/").content)
def getTransactions():
	return json.loads(requests.get("https://www.bitstamp.net/api/transactions/").content)
def getTicker():
	return json.loads(requests.get("https://www.bitstamp.net/api/ticker/").content)
def getAddress(address):
	return chain.get_address(address)

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
	def sell(self, amount):
		price = float(getTicker()['bid'])
		if self.btc < (amount*100000000):
			return False
		self.sells.append({"amount":amount, "price":price})
		self.btc = self.btc - (amount*100000000)
		self.usd = self.usd + (amount * price)
		
## Testing stuff here
def test():
	orders = getOrderBook()
	transactions = getTransactions()
