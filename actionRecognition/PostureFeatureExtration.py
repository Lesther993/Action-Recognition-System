
import math
import os
import numpy as np
from pykinect.nui import JointId
import pykinect
from pykinect import nui
from TorsoCalcutatorModule import calculateTorso

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def jointsDetection(skeleton, dispInfo):

	hipCenterCoord = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.HipCenter], dispInfo.current_w, dispInfo.current_h)
	shoulderCenterCoord = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ShoulderCenter], dispInfo.current_w, dispInfo.current_h)
	#TORSO
	Jo = calculateTorso(hipCenterCoord, shoulderCenterCoord)
	#HEAD
	J1 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
	#NECK which is the same as shoulder center
	J2 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ShoulderCenter], dispInfo.current_w, dispInfo.current_h)
	#ELBOW RIGHT
	J3 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ElbowRight], dispInfo.current_w, dispInfo.current_h)
	#ELBOW LEFT
	J4 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ElbowLeft], dispInfo.current_w, dispInfo.current_h)
	#WRIST RIGHT
	J5 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.WristRight], dispInfo.current_w, dispInfo.current_h)
	#WRIST LEFT
	J6 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.WristLeft], dispInfo.current_w, dispInfo.current_h)
	#KNEEL RIGHT
	J7 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.KneeRight], dispInfo.current_w, dispInfo.current_h)
	#KNEEL LEFT
	J8 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.KneeLeft], dispInfo.current_w, dispInfo.current_h)
	#ANKLE RIGHT
	J9 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.AnkleRight], dispInfo.current_w, dispInfo.current_h)
	#ANKLE LEFT
	J10 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.AnkleLeft], dispInfo.current_w, dispInfo.current_h)

	#Don't consider the joints below yet
	
	#SHOULDER RIGHT																	
	J11 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ShoulderRight], dispInfo.current_w, dispInfo.current_h)
	#SHOULDER LEFT																	
	J12 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.ShoulderLeft], dispInfo.current_w, dispInfo.current_h)
	#HIP RIGHT																	
	J13 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.HipRight], dispInfo.current_w, dispInfo.current_h)
	#HIP LEFT																	
	J14 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.HipLeft], dispInfo.current_w, dispInfo.current_h)
	#SPINE
	J15 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.Spine], dispInfo.current_w, dispInfo.current_h)
	#HAND RIGHT
	J16 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.HandRight], dispInfo.current_w, dispInfo.current_h)
	#HAND LEFT
	J17 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.HandLeft], dispInfo.current_w, dispInfo.current_h)
	#FOOT RIGHT
	J18 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.FootRight], dispInfo.current_w, dispInfo.current_h)
	#FOOT LEFT
	J19 = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.FootLeft], dispInfo.current_w, dispInfo.current_h)

	return [Jo, J1, J2, J3, J4, J5, J6, J7, J8, J9, J10] #Arreglo 1x11x2


def jointsNormalization(joints):
	J = joints[1:]
	Jo = joints[0]
	J2 = joints[2]
	f=[]

	try:
		for Ji in J:
				dx = (Ji[0]-Jo[0])/math.sqrt( ((J2[0]-Jo[0])**2) + ((J2[1]-Jo[1])**2) )
				dy = (Ji[1]-Jo[1])/math.sqrt( ((J2[0]-Jo[0])**2) + ((J2[1]-Jo[1])**2) )
				di = [dx, dy]
				f.append(di)
	except:
		pass

	return f


def saveTrainingData(data, activity):
	try:
		os.mkdir("actionRecognition/PostureFeatures")
	except:
		pass
	data2D = np.array([ data ])
	nsamples, nx, ny = data2D.shape
	data2D = data2D.reshape((nsamples, nx*ny)).tolist()[0]
	fo = open('actionRecognition/PostureFeatures/'+activity+'.txt', 'a+')
	fo.write(str(data2D)+'\n')
	fo.close()