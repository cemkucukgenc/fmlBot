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
mqtt = FMLMqtt("mqttBroker","gruppeX/robot")
line_controller = PIController(0,0.00,0)

done = False
current_task_number = -1

with FMLRobot() as robot:
    while not dgone:
        # reset current taks number
        current_task_number = -1
        
        # TODO add code to read in the task number somehow and drive between the tasks
        
        if current_task_number == 1:
            task_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
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
        
