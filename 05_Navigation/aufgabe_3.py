import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController

controller = PIController(kp=4.0,ki=0.02,target_value=15.0)


with FMLRobot() as robot:
    robot.bypass_obstacle(controller=controller, velocity=200.0)