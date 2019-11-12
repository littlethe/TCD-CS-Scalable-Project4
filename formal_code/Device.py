import threading
import random
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

class Device:
    ID = ''
    SendingClient = None
    SubcribingClient = None
    SendingTimer = None
    SendingInterval = 1 #second
    RandomMinimum = 50
    RandomMaximum = 150
    RandomIsInt   = False
    BrokerIP = '127.0.0.1'
    BrokerPort = 1883
    ConnectionAlive = 1200
    #Topic = 'topic/test'
    Target = None
    IsSender = False
    IsReceiver = False
    BatteryDecline= 0.001 #per second
    Battery = 1
    SelfTimer = None
    
    def __init__(self,ID,target=None):
        self.ID = ID
        self.Target = target
        self.SelfTimer = threading.Timer(1,self.selfAction)

    def selfAction(self):
        self.Battery -= self.BatterDecline
        if(self.Battery <= 0):
            self.stop()
        else:
            self.SelfTimer = threading.Timer(1,self.selfAction)        

    def startSendingTimer(self):
        if (elf.SendingTimer == None):
            print('The timer needs to be set.')
        else:
            self.SendingTimer.start()

    def cancelSendingTimer(self):
        if (self.SendingTimer == None):
            print('The timer needs to be set.')
        else:
            self.PulishingTimer.cancel()
            
    def run(self):
        self.runSending()
        self.runReceiving()

    def runSending(self):
        if(self.IsSender):
            print('Sending to ',self.Target)
            self.SendingClient = mqtt.Client(self.ID)
            self.SendingClient.connect(self.BrokerIP,self.BrokerPort,self.ConnectionAlive)
            self.refreshSendingTimer()

    def runReceiving(self):
        if(self.IsReceiver):
            print('Receiving ',self.ID)
            self.ReceivingClient = mqtt.Client(self.ID)
            self.ReceivingClient.connect(self.BrokerIP,self.BrokerPort,self.ConnectionAlive)
            self.ReceivingClient.on_connect = self.on_connect
            self.ReceivingClient.on_message = self.on_message
            self.ReceivingClient.loop_start()

    def refreshSendingTimer(self):
        self.SendingTimer = threading.Timer(self.SendingInterval,self.SendingAction)
        self.SendingTimer.start()      
        
    def stop(self):
        if(self.SendingClient != None):
            self.SendingClient.disconnect()
        if(self.SubscrbingClient != None):
            self.ReceivingClient.loop_stop()
            self.SubscrbingClient.disconnect()
        if(self.SendingTimer != None):
            self.SendingTimer.cancel()
        if(self.SelfTimer != None):
            self.SelfTimer.cancel()

    def SendingAction(self):
        if(self.IsSender):
            jsonString = self.createJSONString()
            print('To '+self.Target+':'+jsonString)
            self.SendingClient.publish(self.Target, jsonString)
        self.refreshSendingTimer()

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
        self.ReceivingClient.subscribe(self.ID)

    def on_message(self,client, userdata, message):
        jsonString = message.payload.decode()
        #print(jsonString)
        content = json.loads(jsonString)
        #print(message.topic+'-'+content['ID']+':'+content['MESSAGE']+' '+content['TIME'])
        print('From '+content['ID']+':'+str(content['VALUE'])+' '+content['TIME'])

    def createJSONString(self):
        data = self.getRandomNumber()
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #time = datetime.now()
        jsonString = '{"ID":"'+self.ID+'","VALUE":'+str(data)+',"BATTERY":'+str(self.Battery)+',"TIME":"'+time+'"}'
        return jsonString
