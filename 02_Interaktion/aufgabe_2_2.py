import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt
import time


mqtt = FMLMqtt(broker_ip="192.168.0.99", topic="gruppeX/color")

with FMLRobot() as robot:
    pass

# Short MQTT usage info: 
# msg = mqtt.read() waits until it receives a msg in the topic and stores it in the msg
# mqtt.pub("Somestring") publishes "Somestring" to the topic chosen when creating the mqtt object

