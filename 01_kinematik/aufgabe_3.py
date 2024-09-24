import sys

sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time
import numpy as np
import math

points = [np.array([0.4,0.0]), np.array([0.4,0.4]), np.array([0.0,0.4]), np.array([0.0,0.0])]
#robots starts at (0,0) facing x direction
orientation = np.array([1,0]) 
current_position = np.array([0,0]) 


with FMLRobot() as robot:
    for point in points:
        # convert to numpy array for easier computation
        point = np.array(point)

        # Find vector where robot needs to drive to
        to_drive_to = point - current_position
        
        # compute the dot product to get the angle the robot needs to turn
        q1_norm = np.linalg.norm(orientation)  # Magnitude of current orientation vector
        q2_norm = np.linalg.norm(to_drive_to)  # Magnitude of the vector to the waypoint
        dot_product = np.dot(orientation, to_drive_to)
        
        # Actually compute the angle it needs to turn
        angle = np.arccos(dot_product / (q1_norm * q2_norm))

        # check if turning needs to happen as a left or right turn
        determinant = orientation[0]*to_drive_to[1] - orientation[1]*to_drive_to[0]
        if determinant < 0:
            angle *=-1
        
        # compute the length the robot needs to drive 
        length = np.linalg.norm(to_drive_to)
        
        # Now let the robot turn and drive forward
        robot.turn(np.degrees(angle))
        robot.drive(length)
        
        # Update the position for the computation of the next point
        current_position = point

        # Rotate the Orientation vector the same angle the robot has rotated via a rotation Matrix
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        orientation = np.dot(rotation_matrix,orientation)
