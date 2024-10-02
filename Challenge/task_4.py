import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLController import PIController
from FMLCamera import FMLCamera
from FMLMqtt import FMLMqtt
import time

AVAILABLE_FORMS = ["Circle", "Rectangle", "Triangle", "Ellipse"]

def doTask(robot : FMLRobot,mqtt : FMLMqtt,camera: FMLCamera):
    robot.drive(distance=0.05, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line(velocity=300, controller=controller_line_following)


    # Define the MQTT broker address and topic
    broker_address = "mqttbroker"  # Replace with the actual broker IP address or hostname
    topic = "Robot6/shape"

    # Create an MQTT client instance and connect to the broker
    mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

    # Try to connect to the MQTT broker
    if mqtt_client.connect():
        print("Connected to MQTT broker! Waiting for shapes...")

        # Continuously read messages
        while True:
            # Read the shape message from the MQTT broker
            received_shape = mqtt_client.read_message()

            # If a shape is received, print it
            if received_shape:
                print(f"Received shape: {received_shape}")
                break

            # Add a small delay to prevent overwhelming the broker with requests
            time.sleep(0.5)
    else:
        print("Failed to connect to MQTT broker.")

    robot.drive(distance=0.1, velocity=300)
    controller_line_following = PIController(kp=7.0,ki=0.02,target_value=30.0)
    robot.follower_line_short_distance(velocity=300, controller=controller_line_following)
    # print("Drive Stop At Color Working")
    # robot.drive_stop_at_color(velocity=300)
    robot.turn(-90)
    

    # Disconnect when finished
    mqtt_client.disconnect()

    return received_shape

















# import sys
# import time
# sys.path.append("..")
# sys.path.append(".")
# from FMLRobot import FMLRobot
# from FMLMqtt import FMLMqtt

# # Function to check consecutive color readings for reliability
# def detect_reliable_color(robot, mqtt_client, topic):
#     previous_color = robot.get_color_left()  # Get the initial color
#     time.sleep(0.5)  # Short delay between readings
    
#     while True:
#         current_color = robot.get_color_left()  # Read the current color
        
#         if current_color == previous_color:
#             if current_color != "Unknown":
#                 message = f"Color {current_color} detected reliably"
#                 mqtt_client.publish(message)  # Publish the reliable color detection
#         else:
#             mqtt_client.publish("Color not reliably detected")
        
#         # Update previous color to current one for the next comparison
#         previous_color = current_color

#         # Add a delay to avoid reading the sensor too fast
#         time.sleep(0.5)

#         # Check for an incoming message to stop the script
#         received_message = mqtt_client.read_message()
#         print("Received message: {}".format(received_message))
#         if received_message == "color detected correctly":
#             print("Stopping script as 'color detected correctly' message was received.")
#             break

# # MQTT broker configuration
# broker_address = "mqttbroker"  # Replace with your local MQTT broker's IP address
# topic = "group6/color"

# # Initialize the MQTT client
# mqtt_client = FMLMqtt(broker_address, broker_port=1884, topic=topic)

# # Try to connect to the MQTT broker
# if mqtt_client.connect():
#     print("Connection successful! Proceeding with MQTT operations...")
    
#     with FMLRobot() as robot:
#         # Detect color and publish it to the MQTT broker
#         detect_reliable_color(robot, mqtt_client, topic)
    
# else:
#     print("Failed to connect to MQTT broker. Exiting.")

# # Gracefully disconnect after stopping
# mqtt_client.disconnect()
