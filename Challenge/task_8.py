import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import math
import numpy as np
import time

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    robot.turn(-48)
    robot.drive(distance=0.20, velocity=300)
    start_time = time.time()
    
    while True:
        robot.BP.set_motor_dps(robot.left_motor, 300)
        robot.BP.set_motor_dps(robot.right_motor, 300)

        # robot.drive(distance=0.1, velocity=300)
        front_distance = robot.get_distance_front()

        if front_distance <= 15:
            print("Obstacle detected. Waiting for 5 seconds")
            robot.stop()
            robot.BP.set_motor_dps(robot.left_motor, 0)
            robot.BP.set_motor_dps(robot.right_motor, 0)
            time.sleep(5)

        
        # Check if 10 seconds have passed since the start
        elapsed_time = time.time() - start_time
        if elapsed_time >= 20:
            ground_cam_left = robot.get_ground_cam_left()
            if ground_cam_left == "Blue":
                print(f'Detected color: {ground_cam_left}')
                robot.drive(distance=0.08, velocity=300)
                robot.stop()
                break

        
        # ground_cam_left = robot.get_ground_cam_left()
        # if ground_cam_left == "Blue":
        #     blue_count +=1
        #     print('detected color: {}'.format(ground_cam_left))
        #     robot.stop()
        #     break
        #     # if blue_count > 20:
        #     #     robot.stop()
        #     #     break


