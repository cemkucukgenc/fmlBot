import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
from FMLController import PIController
import time

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):

    while True:
        green_percentage = camera.get_green_percentage()
        print(f"Detected green percentage: {green_percentage:.2f}%")
        
        if green_percentage > 10:  # Threshold for green detection
            print("Green image detected. Starting line following.")
            break
        
        # time.sleep(1)  # Wait for 1 second before checking again
        
    # After detecting green, start line following
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)