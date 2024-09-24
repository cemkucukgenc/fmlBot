import sys

sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time
import numpy as np
import math

points = [np.array([0.4,0]), np.array([0.4,.4]), np.array([0,.4]), np.array([0.,0.])]
#robots starts at (0,0) facing x direction
ortientation = np.array([1,0]) 
current_position = np.array([0,0]) 


with FMLRobot() as robot:
    for point in points:
        # convert to numpy array for easier computation
        point = np.array(point)

        # Find vector where robot needs to drive to
        to_drive_to = None
        
        # compute the dot product to get the angle the robot needs to turn
        dot_product = None
        
        # Actually compute the angle it needs to turn
        angle = None

        # check if turning needs to happen as a left or right turn
        determinant = ortientation[0]*to_drive_to[1] - ortientation[1]*to_drive_to[0]
        if determinant < 0:
            angle *=-1
        
        # compute the length the robot needs to drive 
        length = None
        
        # Now let the robot turn and drive forward

        
        # Update the position for the computation of the next point
        current_position= None

        # Rotate the Orientation vector the same angle the robot has rotated via a rotation Matrix
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        ortientation = np.dot(rotation_matrix,ortientation)


