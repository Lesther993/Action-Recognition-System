import pygame
from pygame.color import THECOLORS
import itertools
import pykinect
from pykinect import nui
from pykinect.nui import JointId
from actionRecognition.TorsoCalcutatorModule import calculateTorso
from actionRecognition import PostureFeatureExtration

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image


def drawSkeleton(screen, dispInfo, skeleton, index=0):
    #HEAD
    drawHead(screen,dispInfo,skeleton,index)
    #SPINE
    drawSpine(screen, dispInfo, skeleton, index)
    #LIMBS
    drawLimbs(screen, dispInfo, skeleton, index, LEFT_ARM)
    drawLimbs(screen, dispInfo, skeleton, index, RIGHT_ARM)
    drawLimbs(screen, dispInfo, skeleton, index, LEFT_LEG)
    drawLimbs(screen, dispInfo, skeleton, index, RIGHT_LEG)
    #ALL RELEVANT JOINTS
    drawJoints(screen, dispInfo, skeleton)
    #TORSO
    drawTorso(screen, dispInfo, skeleton)


def drawHead(screen, dispInfo, skeleton,index):
	HeadPos = skeleton_to_depth_image(skeleton.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h)
	pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)

def drawSpine(screen, dispInfo, pSkelton, index):
	drawLimbs(screen, dispInfo, pSkelton, index, SPINE,8)


def drawLimbs(screen, dispInfo, pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def drawJoints(screen, dispInfo, skeleton):
    joints = PostureFeatureExtration.jointsDetection(skeleton, dispInfo)
    for joint in joints :
        pygame.draw.circle(screen, SKELETON_COLORS[2], (int(joint[0]), int(joint[1])), 6, 0)


def drawTorso(screen, dispInfo, skeleton):
    torso = PostureFeatureExtration.jointsDetection(skeleton, dispInfo)[0]
    pygame.draw.circle(screen, SKELETON_COLORS[5], (int(torso[0]), int(torso[1])), 6, 0)  