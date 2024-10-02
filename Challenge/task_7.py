import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import cv2
import numpy as np
import time
from FMLController import PIController

target_shape = "Circle"  # Define the target shape

# Function to detect shapes in the image
def detect_shapes(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise and improve shape detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold the image to create a binary image
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    shapes = []  # List to hold detected shapes

    # Loop through all the contours found
    for contour in contours:
        # Filter out small contours based on the contour area
        if cv2.contourArea(contour) < 1000:
            continue

        # Approximate the contour to remove minor variations
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Determine the shape of the contour based on its approximated vertices
        if len(approx) == 3:
            shapes.append("Triangle")
        elif len(approx) == 4:
            # Check if the shape is square or rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shapes.append("Square")
            else:
                shapes.append("Rectangle")
        elif len(approx) > 4:
            shapes.append("Circle")

    return shapes

# Function to check the shape and move the robot accordingly
def shape_check_and_move(robot, camera, target_shape):
    # Capture an image using the camera
    image = camera.get_image_array()
    
    # Detect shapes in the captured image
    detected_shapes = detect_shapes(image)
    
    # Check if the target shape is in the detected shapes
    if target_shape in detected_shapes:
        print(f"Target shape '{target_shape}' detected. Moving forward.")
        # Move the robot forward
        robot.drive(0.1, 300)  # Drive 0.5 meters forward at speed 300
    else:
        print(f"Target shape '{target_shape}' not detected. Not moving forward.")

# Function to handle behavior when the ground camera detects blue color
def turn_right_at_blue(robot, camera):
    time.sleep(0.1)
    ground_cam_left = robot.get_ground_cam_left()

    if ground_cam_left == "Blue":
        print(f"Detected color: {ground_cam_left}")

        # Turn the robot right and check for shapes
        robot.turn(90)
        
        # Call the shape check and move function
        shape_check_and_move(robot, camera, target_shape)
        
        # Turn the robot back to its original direction
        robot.turn(-90)

    # Continue line following after shape detection
    robot.drive(distance=0.05, velocity=300)
    
    controller_line_following = PIController(kp=7.0, ki=0.02, target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)

# Main task function for the robot
def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera, received_shape):
    # Call the turn_right_at_blue function to perform the sequence
    turn_right_at_blue(robot, camera)





# import sys
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# from FMLCamera import FMLCamera
# from FMLMqtt import FMLMqtt
# import cv2
# import numpy as np
# import time

# target_shape = "Triangle"  # Define the target shape

# # Function to detect shapes in the image
# def detect_shapes(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply Gaussian Blur to reduce noise and improve shape detection
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
#     # Threshold the image to create a binary image
#     _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    
#     # Find contours in the thresholded image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     shapes = []  # List to hold detected shapes

#     # Loop through all the contours found
#     for contour in contours:
#         # Filter out small contours based on the contour area
#         if cv2.contourArea(contour) < 1000:
#             continue

#         # Approximate the contour to remove minor variations
#         epsilon = 0.04 * cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, epsilon, True)

#         # Determine the shape of the contour based on its approximated vertices
#         if len(approx) == 3:
#             shapes.append("Triangle")
#         elif len(approx) == 4:
#             # Check if the shape is square or rectangle
#             x, y, w, h = cv2.boundingRect(approx)
#             aspect_ratio = float(w) / h
#             if 0.95 <= aspect_ratio <= 1.05:
#                 shapes.append("Square")
#             else:
#                 shapes.append("Rectangle")
#         elif len(approx) > 4:
#             shapes.append("Circle")

#     return shapes

# def turn_right_at_blue(robot, camera):
#     time.sleep(0.1)
#     ground_cam_left = robot.get_ground_cam_left()

#     if ground_cam_left == "Blue":
#         print(ground_cam_left)
#         print('detected color: {}'.format(ground_cam_left))

#         robot.turn(90)
#         shape_check = shape(camera, robot)
#         compare_qr_code(qr_code_payload_check, target_payload_ID, robot)
#         robot.turn(-90)

    
#     robot.drive(distance=0.05, velocity=300)
#     controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
#     robot.follower_line(velocity=300, controller=controller_line_following)

# # Main task function for the robot
# def doTask(robot: FMLRobot, mqtt: FMLMqtt, camera: FMLCamera, received_shape):
#     # Capture an image using the camera
#     image = camera.get_image_array()
    
#     # Detect shapes in the captured image
#     detected_shapes = detect_shapes(image)

#     print
    
#     # Check if the target shape is in the detected shapes
#     if target_shape in detected_shapes:
#         print(f"Target shape '{target_shape}' detected. Moving forward.")
#         # Move the robot forward
#         robot.drive(0.5, 300)  # Drive 0.5 meters forward at speed 300
#     else:
#         print(f"Target shape '{target_shape}' not detected.")










# # import sys
# # sys.path.append("..")
# # sys.path.append(".")
# # from FMLRobot import FMLRobot
# # from FMLController import PIController
# # from FMLCamera import FMLCamera
# # from FMLMqtt import FMLMqtt
# # import time

# # def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
# #     pass



# # # import cv2
# # # import numpy as np

# # # def detect_shapes(image_path, output_path="output.png"):
# # #     # Load the image
# # #     image = cv2.imread(image_path)
# # #     height, width = image.shape[:2]

# # #     # Define the Region of Interest (ROI) based on the location of the paper
# # #     # This can be adjusted according to the image dimensions
# # #     roi = image[int(height*0.3):int(height*0.9), int(width*0.1):int(width*0.9)]

# # #     # Convert the ROI to grayscale
# # #     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
# # #     # Apply Gaussian Blur to reduce noise and improve shape detection
# # #     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
# # #     # Threshold the image to create a binary image
# # #     _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    
# # #     # Find contours in the thresholded image
# # #     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
# # #     # Loop through all the contours found
# # #     for contour in contours:
# # #         # Filter out small contours based on the contour area
# # #         if cv2.contourArea(contour) < 1000:
# # #             continue

# # #         # Approximate the contour to remove minor variations
# # #         epsilon = 0.04 * cv2.arcLength(contour, True)
# # #         approx = cv2.approxPolyDP(contour, epsilon, True)

# # #         # Get the shape of the contour based on its approximated vertices
# # #         if len(approx) == 3:
# # #             shape = "Triangle"
# # #         elif len(approx) == 4:
# # #             # Check if the shape is square or rectangle
# # #             x, y, w, h = cv2.boundingRect(approx)
# # #             aspect_ratio = float(w) / h
# # #             if 0.95 <= aspect_ratio <= 1.05:
# # #                 shape = "Square"
# # #             else:
# # #                 shape = "Rectangle"
# # #         elif len(approx) > 4:
# # #             shape = "Circle"
# # #         else:
# # #             shape = "Unknown"

# # #         # Draw the contour and shape name on the ROI
# # #         cv2.drawContours(roi, [approx], -1, (0, 255, 0), 2)
# # #         x, y = approx.ravel()[0], approx.ravel()[1] - 10
# # #         cv2.putText(roi, shape, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # #     # Place the ROI back in the original image
# # #     image[int(height*0.3):int(height*0.9), int(width*0.1):int(width*0.9)] = roi

# # #     # Save the image with detected contours and labels
# # #     cv2.imwrite(output_path, image)
# # #     print(f"Processed image saved as {output_path}")


# # # # Example usage
# # # detect_shapes("images/shapes.png", "images/detected_shapes.png")
