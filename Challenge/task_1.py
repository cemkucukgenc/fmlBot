import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    print("task1 executing")
