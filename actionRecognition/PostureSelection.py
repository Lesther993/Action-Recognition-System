import ast
from sklearn.cluster import KMeans
import numpy as np

def loadTrainingData(activity):
	activityVector=[]
	fo = open('actionRecognition/PostureFeatures/'+activity+'.txt', 'a+')
	data = fo.readlines()
	fo.close()
	for postureVector in data:
		postureVector.strip()
		activityVector.append(ast.literal_eval(postureVector))
	# print activityVector
	return activityVector


def createClusters(activityVector, numberOfClubsters):
	X = np.array(activityVector)
	kmeans = KMeans(n_clusters=numberOfClubsters, random_state=0).fit(X)
	centroids = kmeans.cluster_centers_.tolist()
	fo = open('actionRecognition/Clusters.txt', 'a+')
	for centroid in centroids:
		fo.write(str(centroid)+'\n')
	fo.close()
