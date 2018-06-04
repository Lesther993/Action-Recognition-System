from web3 import Web3, HTTPProvider

import environment

from Clusters import clusters
from ActivityWords import words


import json

web3 = Web3(HTTPProvider(environment.nodeURL))

unicorns = web3.eth.contract(address=environment.contractAddress, abi=json.loads(environment.contractABI))



def saveClusters():
	lot = environment.lot

	formatedClusters = [multiplyByPRecision(x) for x in clusters]
	
	unicorn_txn = unicorns.functions.saveClusters(formatedClusters[(5*lot)-5],formatedClusters[(5*lot)-4],formatedClusters[(5*lot)-3],formatedClusters[(5*lot)-2],formatedClusters[(5*lot)-1]).buildTransaction({
																							'gas': 2500000,
																							'gasPrice': web3.eth.gasPrice,
																							'nonce': web3.eth.getTransactionCount(environment.address_from)})

	signed_txn = web3.eth.account.signTransaction(unicorn_txn, private_key=environment.privateKey)

	tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)  

	print ('Clusters data sent to Blockchain. Tx hash:',tx_hash.hex())

	print('Wating for confirmation...')

	print ('Clusters data confirmed at block:',web3.eth.waitForTransactionReceipt(tx_hash).blockNumber)



def saveWords():

	unicorn_txn = unicorns.functions.saveWords(words[0].values()[0], words[0].keys()[0],words[1].keys()[0],words[2].keys()[0],words[3].keys()[0]).buildTransaction({
																							'gas': 2500000,
																							'gasPrice': web3.eth.gasPrice,
																							'nonce': web3.eth.getTransactionCount(environment.address_from)})

	signed_txn = web3.eth.account.signTransaction(unicorn_txn, private_key=environment.privateKey)

	tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)  

	print ('Word data sent to Blockchain. Tx hash:',tx_hash.hex())

	print ('Word data confirmed at block:',web3.eth.waitForTransactionReceipt(tx_hash).blockNumber)



def loadClusters():
	clusters=[]
	totalClusters =  unicorns.functions.totalClusters().call()
	for i in range(25):
		clusters.append(unicorns.functions.loadClusters(i).call())
	formatedClusters = [divideByPRecision(x) for x in clusters]
	return formatedClusters



def multiplyByPRecision(_clusters):
	return [round(x*environment.precision) for x in _clusters]
	# return round((10**10)*_clusters)

def divideByPRecision(_clusters):
	return [(x/environment.precision) for x in _clusters]
	# return round((10**10)*_clusters)