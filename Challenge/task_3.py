from operator import ne
import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from dijkstra import *
import time


def go_to_color(robot, color_list, ground_cam_left):

    len_color_list = len(color_list)
    i = 0
    while i < len_color_list-1:
        target_color = color_list[i]
        print ("Next point is : {}".format(target_color))

        print ("Color {} searching".format(target_color))
        robot.turn(20)
        time.sleep(0.1)
        ground_cam_left = robot.get_ground_cam_left()
        print(f'detected color: {ground_cam_left}')

        if ground_cam_left == target_color:
            print("Target color: {} found".format(ground_cam_left))
            robot.turn(-5)
            robot.drive(distance=0.10, velocity=300)
            time.sleep(0.5)
            controller_line_following = PIController(kp=7.0, ki=0.02, target_value=30.0)
            robot.follower_line(velocity=200, controller=controller_line_following)
            i = i+1

            # Update ground_cam_left after moving
            ground_cam_left = robot.get_ground_cam_left()
            if ground_cam_left == "Red" or ground_cam_left == "Yellow" or ground_cam_left == "Green" or ground_cam_left == "Blue":
                print("Red stop sign detected but passing")
                robot.drive(distance=0.21, velocity=300)
    

def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera):
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0, ki=0.02, target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)
    
    time.sleep(0.1)
    ground_cam_left = robot.get_ground_cam_left()
    print(f'detected color: {ground_cam_left}')

    if ground_cam_left == "Red" or ground_cam_left == "Yellow" or ground_cam_left == "Green" or ground_cam_left == "Blue":
        print("Red stop sign detected but passing")
        robot.drive(distance=0.21, velocity=300)

    while True:
        start_point = "a"
        end_point = "n"
        color_list = get_path_color_list(start_point, end_point, graph, path_colors)
        print(color_list)
        
        # Pass the ground_cam_left value to the go_to_color function
        go_to_color(robot, color_list, ground_cam_left)




