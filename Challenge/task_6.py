import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time


def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    robot.turn(10)
    robot.drive(distance=0.1, velocity=300)
    controller_bypass_obstacle = PIController(kp=10.0,ki=0.07,target_value=15.0)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.bypass_obstacle(controller_line_following=controller_line_following, controller_bypass_obstacle=controller_bypass_obstacle, velocity=300.0)

    while True:
        robot.wait()