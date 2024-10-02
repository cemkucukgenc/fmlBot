import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time


def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):

    frame = camera.get_image_array()
    frame_height, frame_width, _ = frame.shape
    frame_center_x = frame_width / 2
    frame_center_y = frame_height / 2

    # Print frame details
    # print(f"Frame dimensions: width = {frame_width}, height = {frame_height}")
    # print(f"Frame center: x = {frame_center_x}, y = {frame_center_y}")

    step_distance = 0.1
    turn_angle = 30

    while True:
        qr_position = camera.get_qr_position()
        print(qr_position)

        ground_cam_left = robot.get_ground_cam_left()
        if ground_cam_left == "Red":
            break

        if qr_position is not None:
            # Extract the x position from the QR code position
            x_position = qr_position[0]  # Horizontal position
            print(f"QR Code position: x = {x_position}")
            if x_position > 10:
                print("left")
                robot.turn(-turn_angle)
                time.sleep(0.1)
                robot.drive(step_distance, velocity=300)

            if x_position < -10:
                print("right")
                robot.turn(turn_angle)
                time.sleep(0.1)
                robot.drive(step_distance, velocity=300)

            else: 
                print("straight")
                robot.drive(step_distance, velocity=300)

            
