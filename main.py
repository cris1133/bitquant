import requests
import json


def getOrderBook():
	return json.loads(requests.get("https://www.bitstamp.net/api/order_book/").content)
def getTransactions():
	return json.loads(requests.get("https://www.bitstamp.net/api/transactions/").content)
def getTicker():
	return json.loads(requests.get("https://www.bitstamp.net/api/ticker/").content)

