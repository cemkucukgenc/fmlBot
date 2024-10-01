import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PController
import time

robot = FMLRobot()

controller = PController(3,30)
print(robot.follower_line(110,controller))