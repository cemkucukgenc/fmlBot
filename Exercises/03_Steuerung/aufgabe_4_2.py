import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
import time

robot = FMLRobot()

controller = PIController(7.0,0.02,30.0)
print(robot.follower_line(200,controller))