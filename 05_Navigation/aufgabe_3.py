import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController


with FMLRobot() as robot:
    robot.bypass_obstacle()