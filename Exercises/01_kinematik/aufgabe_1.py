import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time



with FMLRobot() as robot:
    robot.drive(0.1)
    robot.drive(-0.1)
    robot.turn(-90)
