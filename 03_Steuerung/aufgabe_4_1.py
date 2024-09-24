import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PController
import time



p_controller = PController(kp=0,target_value=30)
with FMLRobot() as robot:
    robot.follower_line(velocity=110,controller=p_controller)