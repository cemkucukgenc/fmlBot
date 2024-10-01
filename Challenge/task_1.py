import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time

flag_green_seen_once = False

def wait_green(camera, robot):
    while True:
        green_percentage = camera.get_green_percentage()
        print(f"Detected green percentage: {green_percentage:.2f}%")

        global flag_green_seen_once
        
        if green_percentage > 10:  # Threshold for green detection
            print("Green image detected. Starting line following.")
            
            flag_green_seen_once = True
            break
        
    # After detecting green, start line following
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    current_task_number = 1

    global flag_green_seen_once
    if flag_green_seen_once == False:
        wait_green(camera, robot)

    ground_cam_left = robot.get_ground_cam_left()
    if ground_cam_left == "Red":
        print('detected color: {}'.format(ground_cam_left))
        robot.turn(-90)
        # print(camera.get_image_array())
        while True:
            current_task_number = camera.get_barcode()
            if robot.is_integer(current_task_number):  # Check if the returned string is a number
                current_task_number = int(current_task_number)  # Convert to an integer
                break  # Break the loop when a valid integer is obtained
        robot.turn(90)
    
    return current_task_number