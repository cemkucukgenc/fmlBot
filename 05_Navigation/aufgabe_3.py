import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController

controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
controller_bypass_obstacle = PIController(kp=10.0,ki=0.07,target_value=15.0)


with FMLRobot() as robot:
    robot.bypass_obstacle(controller_line_following=controller_line_following, controller_bypass_obstacle=controller_bypass_obstacle, velocity=300.0)