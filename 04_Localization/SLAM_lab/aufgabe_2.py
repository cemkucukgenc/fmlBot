import sys
import time
import math
import curses
import numpy as np
sys.path.append(".")
sys.path.append("..")
import matplotlib.pyplot as plt
from FMLRobot import FMLRobot


# Grid dimensions
GRID_SIZE = 20
RESOLUTION = 0.05  # Each grid cell represents 5 cm
DISTANCE = 0.05
ANGLE = 45
turning = False 

map = np.full((GRID_SIZE, GRID_SIZE), 0.5)  # 0.5 means unknown

# Robot starting position
x_robot_0 = 2
y_robot_0 = 2
phi_robot_0 = 0

x = list() # Start x coordinate list
y = list() # Start y coordinate list

# Define axis limits
plt.axis([0, 10, 0, 10])
plt.axis([0, 10, 0, 10])


def update_map(robot, turning):
    # The robot odometry system starts its pose in x,y,phi = 0 
    # But the initial robot coordinates are given by x_robot_0, y_robot_0, phi_robot_0
    # Calculate the new robot pose by adding the odometry pose to the initial pose
    robot_odom_pose_x = robot.position[0]# Hint: The object robot has a member call position that contains the updated odometry values [x, y, phi]  
    robot_odom_pose_y = robot.position[1]
    robot_odom_pose_phi = robot.position[2]
    
    robot_x = x_robot_0 + robot_odom_pose_x
    robot_y = y_robot_0 + robot_odom_pose_y
    robot_phi = phi_robot_0 + robot_odom_pose_phi
    x.append(robot_x)
    y.append(robot_y)

    # Update the map.
    save_map(map)

def save_map(grid, filename="robot_path.png"):
    """Save the occupancy grid as an image file."""
    plt.imshow(grid, cmap="gray", origin="lower", vmin=0, vmax=1)
    plt.title("Occupancy Grid Map")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.plot(x, y, color = 'b')
    plt.savefig(filename)

def teleop(stdscr, turning):
    # Print instructions with arrows
    instructions = [
        "Teleop mode enabled. Use the arrow keys to control the robot:",
        "    ↑ : Move forward (0.05m)",
        "← : Turn left (45°)            → : Turn right (-45°)",
        "    ↓ : Move backward (0.05m)",
        "Press 'q' to exit."
    ]
    
    # Display instructions in the console
    for idx, line in enumerate(instructions):
        stdscr.addstr(idx, 0, line)
    
    stdscr.refresh()
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.keypad(True)   # Enable arrow keys
    
    with FMLRobot() as robot:
        update_map(robot, turning)
        while True:
            key = stdscr.getch()  # Get key press
            if key == curses.KEY_UP:
                stdscr.addstr(len(instructions) + 1, 0, "Moving forward      ")
                robot.drive(DISTANCE)  # Move forward 0.05 meters
                update_map(robot, turning)
            elif key == curses.KEY_DOWN:
                stdscr.addstr(len(instructions) + 1, 0, "Moving backward     ")
                robot.drive(-DISTANCE)  # Move backward 0.05 meters
                update_map(robot, turning)
            elif key == curses.KEY_LEFT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning left        ")
                robot.turn(ANGLE)  # Turn 45 degrees to the left
                turning = not turning
                update_map(robot, turning)
            elif key == curses.KEY_RIGHT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning right       ")
                robot.turn(-ANGLE)  # Turn 45 degrees to the right
                turning = not turning
                update_map(robot, turning)
            elif key == ord('q'):
                stdscr.addstr(len(instructions) + 1, 0, "Exiting teleop mode.")
                break
            stdscr.refresh()

if __name__ == "__main__":
    turning = False 
    curses.wrapper(teleop, turning)