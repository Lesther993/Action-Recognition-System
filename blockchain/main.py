import uploadToBlockchain
import environment
import ast

environment.address_from = input("Direccion: ")
environment.privateKey = input("Llave privada: ")

saveClusters = ast.literal_eval(input("Guardar clusters en el blockchain?: "))

if saveClusters:
	environment.lot = ast.literal_eval(input("Subir clusters para actividad numero: "))
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