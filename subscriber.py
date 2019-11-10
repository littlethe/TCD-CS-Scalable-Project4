import paho.mqtt.client as mqtt
import json

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/test")

def on_message(client, userdata, message):
  json_str = message.payload.decode()
  content = json.loads(json_str)
  print(content['name']+':'+content['message'])

name = input('Your name?:')

client = mqtt.Client(client_id=name,userdata=name)
client.connect("127.0.0.1",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
