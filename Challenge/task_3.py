from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import dijkstra
import time



color_dict = {'a': "Blue", 'b': "Red", 'c': "Blue", 'd': "Blue", 'e': "Red",
                  'f': "Yellow", 'g': "Blue", 'h': "Yellow", 'i': "Red", 'j': "Red",
                  'k': "Blue", 'l': "Blue", 'm': "Red", 'n': "Yellow", 'o': "Red"}

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)
    
    time.sleep(0.1)
    ground_cam_left = robot.get_ground_cam_left()
    print('detected color: {}'.format(ground_cam_left))

    # while True:
    #     ground_cam_left_from_func = robot.get_ground_cam_left()
    #     print('detected color from func: {}'.format(ground_cam_left_from_func))



    if ground_cam_left == "Red":
        print("Red detected but passing")
        robot.drive(distance=0.21, velocity=300)

    while True:
        robot.turn(15)
        time.sleep(0.1)
        ground_cam_left = robot.get_ground_cam_left()
        print('detected color: {}'.format(ground_cam_left)) 


        target_color = "Blue"  # Define the target color here
        if ground_cam_left == target_color:
            robot.turn(-10)
            robot.drive(distance=0.10, velocity=300)
            time.sleep(0.5)
            controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
            robot.follower_line(velocity=300, controller=controller_line_following)

            ground_cam_left = robot.get_ground_cam_left()
            if ground_cam_left == "Red":
                print("Red stop sign detected but passing")
                robot.drive(distance=0.21, velocity=300)


