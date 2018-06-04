import uploadToBlockchain
import environment
import ast

environment.address_from = input("Address: ")
environment.privateKey = input("Private key: ")

saveClusters = ast.literal_eval(input("Save Clusters on Blockchain?: "))

if saveClusters:
	environment.lot = ast.literal_eval(input("Upload Clusters for activity number: "))
	uploadToBlockchain.saveClusters()
# else:
# 	saveWords = ast.literal_eval(input("Save Words for Activities on Blockchain?: "))

# if saveWords:
# 	uploadToBlockchain.saveWords()


# import requests
# import json

# dicOfWords={}
# r = requests.post("http://localhost:4200/action-recognition/loadWords")
# data = json.loads(r.content)[u'data']
# for word in data:
# 	dicOfWords[str(word[u'word'])] = str(word[u'name'])
# print dicOfWords


# r = requests.post("http://localhost:4200/action-recognition/loadClusters")
# clusters = json.loads(r.content)[u'data'].values()[0]
# print clusters