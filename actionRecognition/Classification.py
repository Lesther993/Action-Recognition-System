import ast
import difflib
import settings
import requests
import json

def loadWords():
	print('Loading words')
	dicOfWords={}
	if settings.blockchain:
		r = requests.post("http://localhost:4200/action-recognition/loadWords")
		data = json.loads(r.content)[u'data']
		print('Words loaded from blockchain')
		for word in data:
			dicOfWords[str(word[u'word'])] = str(word[u'name'])
	else:
		fo = open('actionRecognition/ActivityWords.txt', 'a+')
		data = fo.readlines()
		print('Words loaded from TXT file')
		for word in data:
			word.strip()
			word = ast.literal_eval(word)
			dicOfWords[word.keys()[0]] = word.values()[0]
	return dicOfWords

def getActivity(dicOfWords, word):
	closestWord = difflib.get_close_matches(word, dicOfWords.keys(),1)
	if len(closestWord)>0:
		activity = dicOfWords[closestWord[0]]
	else:
		activity = 'Unknown'
	return activity
