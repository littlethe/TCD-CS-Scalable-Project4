import threading
import random
import paho.mqtt.client as mqtt
import json
from datetime import datetime

class Device:
    ID = ''
    Client = None
    Timer = None
    TimerInterval = 1 #second
    RandomMinimum = 50
    RandomMaximum = 150
    RandomIsInt   = False
    BrokerIP = '127.0.0.1'
    BrokerPort = 1883
    ConnectionAlive = 120
    #Topic = 'topic/test'
    Topic = 'Health'
    IsSender = False
    IsReceiver = False
    
    def __init__(self,ID=ID):
        self.ID = ID

    def setTimer(self,interval):
        self.Timer = threading.Timer(interval,self.timerAction)

    def startTimer(self):
        if self.Timer == None:
            print('The timer needs to be set.')
        else:
            self.Timer.start()

    def cancelTimer(self):
        if self.Timer == None:
            print('The timer needs to be set.')
        else:
            self.Timer.cancel()

    def run(self):
        if(self.IsSender):
            self.publish()
            self.setTimer(self.TimerInterval)
            self.Timer.start()           
        if(self.IsReceiver):
            self.subscribe()

    def keepRunning(self):
        self.setTimer(self.TimerInterval)
        self.Timer.start()        
        
    def stop(self):
        self.Client.disconnect()
        self.Timer.cancel()

    def timerAction(self):
        if(self.IsSender):
            jsonString = self.createJSONString(self.getRandomNumber())
            self.Client.publish(self.Topic, jsonString)
            print(jsonString)
        self.keepRunning()

    def printID(self):
        print(self.ID)

    def getRandomNumber(self):
        if(self.RandomIsInt==True):
            value = random.randint(self.RandomMinimum,self.RandomMaximum)
        else:
            value = self.RandomMinimum + random.random()*(self.RandomMaximum-self.RandomMinimum)
        return value

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.Client.subscribe(self.Topic)

    def on_message(self,client, userdata, message):
        jsonString = message.payload.decode()
        content = json.loads(jsonString)
        #print(message.topic+'-'+content['ID']+':'+content['MESSAGE']+' '+content['TIME'])
        print(content['ID']+':'+content['MESSAGE']+' '+content['TIME'])

    def subscribe(self):
        print('Subscribing...')
        self.Client = mqtt.Client(self.ID)
        self.Client.connect(self.BrokerIP,self.BrokerPort,self.ConnectionAlive)
        self.Client.on_connect = self.on_connect
        self.Client.on_message = self.on_message
        self.Client.loop_forever()

    def publish(self):
        print('Publishing...')
        self.Client = mqtt.Client(self.ID)
        self.Client.connect(self.BrokerIP,self.BrokerPort,self.ConnectionAlive)

    def createJSONString(self,data):
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #time = datetime.now()
        jsonString = '{"ID":"'+self.ID+'","MESSAGE":"'+str(data)+'","TIME":"'+time+'"}'
        return jsonString

##a = Device('t')
##a.run()
