from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import dijkstra
import time



color_dict = {'a': "Blue", 'b': "Red", 'c': "Blue", 'd': "Blue", 'e': "Red",
                  'f': "Yellow", 'g': "Blue", 'h': "Yellow", 'i': "Red", 'j': "Red",
                  'k': "Blue", 'l': "Blue", 'm': "Red", 'n': "Yellow", 'o': "Red"}

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    pass