import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time 
import aufgabe_1 
import aufgabe_2
import aufgabe_3 
import aufgabe_4 
import aufgabe_5 
import aufgabe_6 
import aufgabe_7 
import aufgabe_8 


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
            aufgabe_1.doTask(robot,mqtt,camera)
        if current_task_number == 2:
            aufgabe_2.doTask(robot,mqtt,camera)
        if current_task_number == 3:
            aufgabe_3.doTask(robot,mqtt,camera)
        if current_task_number == 4:
            aufgabe_4.doTask(robot,mqtt,camera)
        if current_task_number == 5:
            aufgabe_5.doTask(robot,mqtt,camera)
        if current_task_number == 6:
            aufgabe_6.doTask(robot,mqtt,camera)
        if current_task_number == 7:
            aufgabe_7.doTask(robot,mqtt,camera)
        if current_task_number == 8:
            aufgabe_8.doTask(robot,mqtt,camera)
            done = True
        
