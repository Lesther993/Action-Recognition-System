import ast
import os    
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def ActivityCounter(activity, posture, postureLabel, _counter):
	counter = _counter
	lastPosture = posture

	if postureLabel!=-1:
		if formatLabel(postureLabel)!=lastPosture:
			lastPosture=formatLabel(postureLabel)
			if formatLabel(postureLabel)==postureToDetect(activity):
				counter+=0.5

	return (lastPosture, counter)


def saveActivityCounterData(counter,activity):
	activityFile = activity.title().replace(" ","")
	activityFilePath = 'actionRecognition/' + activityFile +'ActivityHistory.txt'

	if (not os.path.isfile(activityFilePath)) or (os.path.isfile(activityFilePath) and (not os.path.getsize(activityFilePath) > 0)): 
		fo = open(activityFilePath, 'w')
		activityHistory = {'repeticiones': [], 'dias': []}
		fo.write(str(activityHistory)+'\n')
		fo.close()
		
	if os.path.isfile(activityFilePath) and os.path.getsize(activityFilePath) > 0:
		fo = open(activityFilePath, 'r')
		data = fo.readlines()
		_activityHistory = data[0]
		_activityHistory.strip()
		activityHistory = ast.literal_eval(_activityHistory)
		activityHistory['repeticiones'].append(int(counter))
		if len(activityHistory['dias'])==0:
			activityHistory['dias'].append(1)
		else:
			activityHistory['dias'].append( activityHistory['dias'][len(activityHistory['dias'])-1]+1 )
		fo.close()

		fo = open(activityFilePath, 'w')
		# Data for plotting
		t = np.array(activityHistory['dias'])
		s = np.array(activityHistory['repeticiones'])
		fig, ax = plt.subplots()
		ax.plot(t, s)
		ax.set(xlabel='Dias', ylabel='Repeticiones',
		       title='Numero de repeticiones por dia')
		ax.grid()
		fig.savefig(activityFile +'ActivityHistory.png')

		fo.write(str(activityHistory)+'\n')
		fo.close()





def formatLabel(postureLabel):
	return str(unichr(postureLabel+97))

def postureToDetect(activity):
	switcher = {
		# "Waving Right Hand":"g",
		# "Waving Left Hand":"a"
		'Jumping':'y',
		'Jumping Jacks':'f',
		'Squats':'q',
		'Dumbbell Shoulder Press':'m',
		'Biceps Curl':'t',
		'Saltando':'y',
		'Saltos de Tijera':'f',
		'Sentadillas':'q',
		'Prensa de Hombro con Mancuernas':'m',
		'Curl de Biceps':'t'
	}

	pose = switcher.get(activity,'Desconocido')
	if pose=='Desconocido':
		raise Exception('Invalid Activity')

	return pose

