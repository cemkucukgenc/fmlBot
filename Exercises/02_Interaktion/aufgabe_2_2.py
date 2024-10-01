import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt

# Function to check consecutive color readings for reliability
def detect_reliable_color(robot, mqtt_client, topic):
    previous_color = robot.get_color_left()  # Get the initial color
    time.sleep(0.5)  # Short delay between readings
    
    while True:
        current_color = robot.get_color_left()  # Read the current color
        
        if current_color == previous_color:
            if current_color != "Unknown":
                message = f"Color {current_color} detected reliably"
                mqtt_client.publish(message)  # Publish the reliable color detection
        else:
            mqtt_client.publish("Color not reliably detected")
        
        # Update previous color to current one for the next comparison
        previous_color = current_color

        # Add a delay to avoid reading the sensor too fast
        time.sleep(0.5)

        # Check for an incoming message to stop the script
        received_message = mqtt_client.read_message()
        print("Received message: {}".format(received_message))
        if received_message == "color detected correctly":
            print("Stopping script as 'color detected correctly' message was received.")
            break

# MQTT broker configuration
broker_address = "mqttbroker"  # Replace with your local MQTT broker's IP address
topic = "group6/color"

# Initialize the MQTT client
mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# Try to connect to the MQTT broker
if mqtt_client.connect():
    print("Connection successful! Proceeding with MQTT operations...")
    
    with FMLRobot() as robot:
        # Detect color and publish it to the MQTT broker
        detect_reliable_color(robot, mqtt_client, topic)
    
else:
    print("Failed to connect to MQTT broker. Exiting.")

# Gracefully disconnect after stopping
mqtt_client.disconnect()
