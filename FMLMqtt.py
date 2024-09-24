from time import sleep
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt

class FMLMqtt:

    # Simplified interface class for the mqtt access. This class directly subscribes to the topic
    def __init__(self,broker_ip, topic):
        self.topic = topic
        self.broker_ip = broker_ip

    def pub(self,text):
        publish.single(self.topic,payload=text, hostname=self.broker_ip)

    # Blocking function that return the last received message
    def read(self):
        msg = subscribe.simple(self.topic,hostname=self.broker_ip)
        return str(msg.payload.decode("utf-8"))