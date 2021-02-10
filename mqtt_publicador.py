import paho.mqtt.client as mqtt
import json

insert = {"data" : "Hola! Soy el generador de un mensaje :)"}
client = mqtt.Client()
client.connect("localhost", 1883,68)
client.publish("/test_topic",payload=json.dumps(insert),qos=0, retain= False)
