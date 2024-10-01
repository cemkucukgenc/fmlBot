import sys
import time
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt

# MQTT broker configuration
broker_address = "mqttbroker"  # Replace with your MQTT broker's IP address
topic = "group6/fork"

# Initialize the MQTT client
mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)



# Function to process messages from MQTT and move the fork
def process_fork_movement(robot, mqtt_client):
    state = 1 # up
    while True:
        # Wait for a message from the "fork" topic
        message = mqtt_client.read_message()
        print(f"Received message: {message}")
        
        if message == "up" and state == 0:
            print("Lifting fork...")
            robot.lift_fork()  # Call the lift_fork() method to raise the fork
            state = 1
        elif message == "down" and state == 1:
            print("Dropping fork...")
            robot.drop_fork()  # Call the drop_fork() method to lower the fork
            state = 0
        else:
            print(f"No movement")
        
        time.sleep(1)  # Add a delay to prevent overwhelming the system with too many messages

# Try to connect to the MQTT broker
if mqtt_client.connect():
    print("Connection successful! Subscribed to fork topic.")

    # Start controlling the fork based on MQTT messages
    with FMLRobot() as robot:
        process_fork_movement(robot, mqtt_client)
    
else:
    print("Failed to connect to MQTT broker. Exiting.")

# Gracefully disconnect after completion
mqtt_client.disconnect()
