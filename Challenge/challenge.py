import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time 
import task_1 
import task_2
import task_3 
import task_4 
import task_5 
import task_6 
import task_7 
import task_8 


camera = FMLCamera()
mqtt = FMLMqtt("mqttBroker","gruppe6/robot")
line_controller = PIController(0,0.00,0)

done = False
current_task_number = -1

with FMLRobot() as robot:
    while not done:
        # reset current taks number
        
        if current_task_number == -1:
            print("Task -1 Executing")
            controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
            robot.follower_line(velocity=300, controller=controller_line_following)
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
                
        if current_task_number == 1:
            print("Task 1 Executing")
            task_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
            print("Task 2 Executing")
            task_2.doTask(robot,mqtt,camera)
        if current_task_number == 3:
            task_3.doTask(robot,mqtt,camera)
        if current_task_number == 4:
            task_4.doTask(robot,mqtt,camera)
        if current_task_number == 5:
            task_5.doTask(robot,mqtt,camera)
        if current_task_number == 6:
            task_6.doTask(robot,mqtt,camera)
        if current_task_number == 7:
            task_7.doTask(robot,mqtt,camera)
        if current_task_number == 8:
            task_8.doTask(robot,mqtt,camera)
            done = True
        
