import sys
import numpy as np
sys.path.append(".")
sys.path.append("..")
import curses
from FMLRobot import FMLRobot

DISTANCE = 0.05
ANGLE = 45

def teleop(stdscr):
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
        while True:
            key = stdscr.getch()  # Get key press

            if key == curses.KEY_UP:
                stdscr.addstr(len(instructions) + 1, 0, "Moving forward      ")
                # Move forward DISTANCE meters
            elif key == curses.KEY_DOWN:
                stdscr.addstr(len(instructions) + 1, 0, "Moving backward     ")
                # Move backward DISTANCE meters
            elif key == curses.KEY_LEFT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning left        ")
                # Turn ANGLE degrees to the left
            elif key == curses.KEY_RIGHT:
                stdscr.addstr(len(instructions) + 1, 0, "Turning right       ")
                # Turn ANGLE degrees to the right
            elif key == ord('q'):
                stdscr.addstr(len(instructions) + 1, 0, "Exiting teleop mode.")
                break
            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(teleop)