import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time

flag_qr_code_matched = False

def check_qr_code_payload(camera, robot):
    while True:
        qr_code_payload_check = camera.get_barcode()
        if robot.is_integer(qr_code_payload_check):  # Check if the returned string is a number
            qr_code_payload_check = int(qr_code_payload_check)  # Convert to an integer
            print("Detected Payload ID: {}".format(qr_code_payload_check))
            break  # Break the loop when a valid integer is obtained
    return qr_code_payload_check

def compare_qr_code(qr_code_payload_check, target_payload_ID, robot):
    global flag_qr_code_matched
    if qr_code_payload_check == target_payload_ID:
        print("QR Codes Matched")
        flag_qr_code_matched = True
        robot.drive(distance=0.10, velocity=300)
        robot.drop_fork()
        time.sleep(0.1)
        robot.lift_fork()
        time.sleep(0.1)
        robot.drive(distance=-0.10, velocity=300)

def turn_right_at_blue(robot, camera, target_payload_ID, flag_qr_code_matched):
    ground_cam_left = robot.get_ground_cam_left()

    if ground_cam_left == "Blue" or "Green":
        print(ground_cam_left)
        print('detected color: {}'.format(ground_cam_left))

        if not flag_qr_code_matched:
            robot.turn(90)
            qr_code_payload_check = check_qr_code_payload(camera, robot)
            compare_qr_code(qr_code_payload_check, target_payload_ID, robot)
            robot.turn(-90)
    
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)
    

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    current_task_number = 2
    global flag_qr_code_matched
    while flag_qr_code_matched:
        target_payload_ID = camera.get_barcode()
        if robot.is_integer(target_payload_ID):  # Check if the returned string is a number
            target_payload_ID = int(target_payload_ID)  # Convert to an integer
            print("Target Payload ID: {}".format(target_payload_ID))
            break  # Break the loop when a valid integer is obtained
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)


    turn_right_at_blue(robot, camera, target_payload_ID, flag_qr_code_matched)
    turn_right_at_blue(robot, camera, target_payload_ID, flag_qr_code_matched)
    turn_right_at_blue(robot, camera, target_payload_ID, flag_qr_code_matched)

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

