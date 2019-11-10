import paho.mqtt.client as mqtt

# This is the Publisher

name = input('Your name?:')

client = mqtt.Client(client_id=name,userdata=name)
client.connect("127.0.0.1",1883,60)

while(-1):
    message = input('Message:')
    json = '{ "name":"'+name+'", "message":"'+message+'"}'
    print('sent:',json)
    client.publish("topic/test", json);
#client.disconnect();
