import sys
sys.path.append("..")
sys.path.append(".")
from FMLRobot import FMLRobot
from FMLMqtt import FMLMqtt
import time

mqtt = FMLMqtt(broker_ip="192.168.0.99", topic="gruppeX/hubgeruest")
with FMLRobot() as robot:
    pass
