import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("binario/Dormitorio")


def on_message(client,userdata,msg):
    message = json.loads(msg.payload)
    print(message)
    if message["value"] == "on":
        #Turn on lights
        print("Value is ON")
    else:
        #Turn off lights
        print("Value is OFF")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()