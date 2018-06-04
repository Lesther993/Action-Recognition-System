

import thread
import ast

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *
from DrawSkeletonModule import drawSkeleton
import actionRecognition.settings as settings
from actionRecognition.ActionRecognitionModule import actionRecognition, PostureSelectionMethod
import actionRecognition.ActivityFeatureComputation as ActivityFeatureComputation
import actionRecognition.Classification as Classification
import actionRecognition.Counter as Counter

KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 640,480 #320,240
VIDEO_WINSIZE = 640,480

pygame.init()


skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def draw_skeletons(skeletons):
    skeleton = skeletons[0]
    drawSkeleton(screen, dispInfo, skeleton)



def depth_frame_ready(frame):
    with screen_lock:
        if skeletons is not None and draw_skeleton:
            #Recognize action
            actionRecognition(skeletons, dispInfo)
            # Draw skeleton
            draw_skeletons(skeletons)
        pygame.display.update()    


def init():

    settings.training = ast.literal_eval(raw_input("Training phase?: "))
    if settings.training:
        settings.activity = raw_input("Activity to save?: ")
        settings.creatingClusters = ast.literal_eval(raw_input("Creating Clusters?: "))
        if settings.creatingClusters:
            settings.numberOfClubsters = ast.literal_eval(raw_input("Number of Clusters per Activity?: "))
            print("Creating Clusters in Posture Selection phase...")
            PostureSelectionMethod()
        else:
            settings.creatingActivitySequence = ast.literal_eval(raw_input("Creating Activity Sequence?: "))
            if settings.creatingActivitySequence:
                settings.numberOfClubsters = ast.literal_eval(raw_input("Number of Clusters per Activity?: "))
                settings.clusters = ActivityFeatureComputation.loadClusters()
                print("Creating Activity Sequence in Activity Feature Computation phase...")
            else:
                print("Save Training Data in Posture Selection phase...")
    else:
        settings.blockchain = ast.literal_eval(raw_input("Use Activities saved on Blockchain?: "))
        settings.clusters = ActivityFeatureComputation.loadClusters()
        settings.words = Classification.loadWords()
        if settings.blockchain:
            settings.numberOfClubsters = 5
        else:
            settings.numberOfClubsters = ast.literal_eval(raw_input("Number of Clusters per Activity?: "))
        settings.monitorActivity = ast.literal_eval(raw_input("Monitor Activity?: "))
        if settings.monitorActivity:
            settings.activity = raw_input("Activity to monitor?: ")
            print("Monitoring mode...")
        else: 
            print("Test phase...")


    if not (settings.creatingClusters):
        global screen_lock
        global screen
        global dispInfo
        global draw_skeleton
        global skeletons
        full_screen = False
        draw_skeleton = True
        skeletons = None
        kinect = nui.Runtime()
        kinect.skeleton_engine.enabled = True
        screen_lock = thread.allocate()
        screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)    
        pygame.display.set_caption('Python Kinect Demo')
        screen.fill(THECOLORS["black"])

        def post_frame(frame):
            try:
                pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
            except:
                # event queue full
                pass

        kinect.skeleton_frame_ready += post_frame        
        kinect.depth_frame_ready += depth_frame_ready            
        kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

        # main game loop
        done = False

        while not done:
            e = pygame.event.wait()
            dispInfo = pygame.display.Info()
            if e.type == pygame.QUIT:
                done = True
                if settings.monitorActivity:
                    Counter.saveActivityCounterData(settings.counter, settings.activity)
                break
            elif e.type == KINECTEVENT:
                skeletons = e.skeletons
                if draw_skeleton:
                    pygame.draw.rect(screen,THECOLORS["black"],(0,0,DEPTH_WINSIZE[0],DEPTH_WINSIZE[1]))
                    draw_skeletons(skeletons)
                    # print settings.activityDetected
                    activityFont = pygame.font.SysFont("monospace", 25)
                    activityLabel = activityFont.render(settings.activityDetected, 1, (255,255,0))
                    screen.blit(activityLabel, (50, 50)) 
                    if settings.monitorActivity:
                        counterFont = pygame.font.SysFont("monospace", 25)
                        counterLabel = counterFont.render("Repetitions: " + str(int(settings.counter)), 1, (0,255,0))
                        screen.blit(counterLabel, (100, 100))                                                   
                    pygame.display.update()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    if settings.monitorActivity:
                        Counter.saveActivityCounterData(settings.counter, settings.activity)
                    break