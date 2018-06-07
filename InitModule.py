

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

    settings.training = formatInput(raw_input("Etapa de entrenamiento? (Si/No): "))
    if settings.training:
        settings.activity = raw_input("Activividad a guardar?: ")
        settings.creatingClusters = formatInput(raw_input("Crear clusters? (Si/No): "))
        if settings.creatingClusters:
            settings.numberOfClubsters = ast.literal_eval(raw_input("Numero de clusters por actividad?: "))
            print("Creando clusters en etapa de Seleccion de Postura...")
            PostureSelectionMethod()
        else:
            settings.creatingActivitySequence = formatInput(raw_input("Crear secuencia de actividad? (Si/No): "))
            if settings.creatingActivitySequence:
                settings.numberOfClubsters = ast.literal_eval(raw_input("Numero de clusters por actividad?: "))
                settings.clusters = ActivityFeatureComputation.loadClusters()
                print("Creando secuencia de actividad en etapa de Calculo de Rasgos de la Actividad...")
            else:
                print("Guardar data de entrenamiento en etapa de Seleccion de Postura...")
    else:
        settings.blockchain = formatInput(raw_input("Usar actividades guardadas en el Blockchain? (Si/No): "))
        settings.clusters = ActivityFeatureComputation.loadClusters()
        settings.words = Classification.loadWords()
        if settings.blockchain:
            settings.numberOfClubsters = 5
        else:
            settings.numberOfClubsters = ast.literal_eval(raw_input("Numero de clusters por actividad?: "))
        settings.monitorActivity =  formatInput(raw_input("Monitorear actividad? (Si/No): "))
        if settings.monitorActivity:
            settings.activity = raw_input("Actividad a monitorear?: ")
            print("Modo de monitoreo...")
        else: 
            print("Etapa de prueba...")


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
        pygame.display.set_caption('Sistema de reconocimiento de actividades')
        screen.fill(THECOLORS["white"])

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
                    pygame.draw.rect(screen, THECOLORS["white"], (0,0,DEPTH_WINSIZE[0],DEPTH_WINSIZE[1]))
                    draw_skeletons(skeletons)
                    # pygame.font.Font(None,60).set_bold(True)
                    activityFont = pygame.font.SysFont("monospace", 25)
                    activityLabel = activityFont.render(settings.activityDetected, 1, THECOLORS['blue'])
                    screen.blit(activityLabel, (50, 50)) 
                    if settings.monitorActivity:
                        counterFont = pygame.font.SysFont("monospace", 25)
                        counterLabel = counterFont.render("Repeticiones: " + str(int(settings.counter)), 1, THECOLORS['purple'])
                        screen.blit(counterLabel, (100, 100))                                                   
                    pygame.display.update()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    done = True
                    if settings.monitorActivity:
                        Counter.saveActivityCounterData(settings.counter, settings.activity)
                    break



def formatInput(inputValue):
    if inputValue=='Si' or inputValue=='si' or inputValue=='SI':
        return True
    elif inputValue=='No' or inputValue=='no' or inputValue=='NO':
        return False
    else:
        raise Exception("Invalid input value")