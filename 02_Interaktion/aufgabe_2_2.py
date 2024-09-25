import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt

# MQTT broker configuration
broker_address = "mqttbroker"  # Replace with your local MQTT broker's IP address
topic = "groupX/color"

# Initialize the MQTT client
mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# Try to connect to the MQTT broker
if mqtt_client.connect():
    print("Connection successful! Proceeding with MQTT operations...")
    
    # Publish a message to the topic
    # mqtt_client.publish("Hello from main script!")
    
    # Wait for a message to be published and read it
    print("Waiting for a message...")
    # received_message = mqtt_client.read_message()
    # print(f"Received message: {received_message}")
    
else:
    print("Failed to connect to MQTT broker. Exiting.")

# Gracefully disconnect after receiving the message
mqtt_client.disconnect()