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
		activityHistory = {'repetitions': [], 'days': []}
		fo.write(str(activityHistory)+'\n')
		fo.close()
		
	if os.path.isfile(activityFilePath) and os.path.getsize(activityFilePath) > 0:
		fo = open(activityFilePath, 'r')
		data = fo.readlines()
		_activityHistory = data[0]
		_activityHistory.strip()
		activityHistory = ast.literal_eval(_activityHistory)
		activityHistory['repetitions'].append(int(counter))
		if len(activityHistory['days'])==0:
			activityHistory['days'].append(1)
		else:
			activityHistory['days'].append( activityHistory['days'][len(activityHistory['days'])-1]+1 )
		fo.close()

		fo = open(activityFilePath, 'w')
		# Data for plotting
		t = np.array(activityHistory['days'])
		s = np.array(activityHistory['repetitions'])
		fig, ax = plt.subplots()
		ax.plot(t, s)
		ax.set(xlabel='Days', ylabel='Repetitions',
		       title='Number of repetitions per day')
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
		'Biceps Curl':'t'
	}
	return switcher.get(activity,'Unknown')

