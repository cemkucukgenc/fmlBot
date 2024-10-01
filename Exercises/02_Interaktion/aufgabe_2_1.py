import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
import time

# Function to check consecutive color readings for reliability
def detect_reliable_color(robot):
    previous_color = robot.get_color_left()  # Get the initial color
    time.sleep(0.5)  # Short delay between readings
    
    while True:
        current_color = robot.get_color_left()  # Read the current color
        
        if current_color == previous_color:
            if current_color != "Unknown":
                print(f"Color {current_color} detected reliably")
        else:
            print("Color not reliably detected")
        
        # Update previous color to current one for next comparison
        previous_color = current_color

        # Add a delay to avoid reading the sensor too fast
        time.sleep(0.5)

with FMLRobot() as robot:
    detect_reliable_color(robot)

