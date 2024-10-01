import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt

AVAILABLE_FORMS = ["Circle", "Rectangle", "Triangle", "Ellipse"]

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    pass
    