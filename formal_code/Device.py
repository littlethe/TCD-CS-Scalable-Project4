import threading
import random
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

class Device:
    ID = ''
    SendingClient = None
    ReceivingClient = None
    SendingTimer = None
    SendingInterval = 1 #second
    RandomMinimum = 50
    RandomMaximum = 150
    RandomIsInt   = False
    SendingIP = '127.0.0.1'
    SendingPort = 1883
    ReceivingIP = '127.0.0.1'
    ReceivingPort = 1883
    ConnectionAlive = 1200
    SendingTarget = None
    IsSender = False
    IsReceiver = False
    BatteryDecline= 0.001 #per second
    Battery = 1
    SelfTimer = None
    
    def __init__(self,ID,sendingTarget=None,sendingIP='127.0.0.1',receivingIP='127.0.0.1',sendingPort=1883,receivingPort=1883):
        self.ID = ID
        self.SendingTarget = sendingTarget
        self.SendingIP = sendingIP
        self.SendingPort = sendingPort
        self.ReceivingIP = receivingIP
        self.ReceivingPort = receivingPort
        self.SelfTimer = threading.Timer(1,self.selfAction)
        if(self.IsSender):
            self.SendingClient = mqtt.Client(self.ID)
            self.SendingClient.connect(self.SendingIP,self.SendingPort,self.ConnectionAlive)
        if(self.IsReceiver):
            if(self.SendingIP == self.ReceivingIP and self.SendingPort == self.ReceivingPort):
                self.ReceivingClient = self.SendingClient
            else:
                self.ReceivingClient = mqtt.Client(self.ID)
                self.ReceivingClient.connect(self.ReceivingIP,self.ReceivingPort,self.ConnectionAlive)
            self.ReceivingClient.on_connect = self.on_connect
            self.ReceivingClient.on_message = self.on_message

    def selfAction(self):
        self.Battery -= self.BatterDecline
        if(self.Battery <= 0):
            self.stop()
        else:
            self.SelfTimer = threading.Timer(1,self.selfAction)        
            
    def run(self):
        self.runSending()
        self.runReceiving()

    def runSending(self):
        if(self.IsSender):
            print('Sending to ',self.SendingTarget,'.')
            self.refreshSendingTimer()

    def runReceiving(self):
        if(self.IsReceiver):
            print(self.ID,' is receiving.')
            self.ReceivingClient.loop_start()

    def refreshSendingTimer(self):
        self.SendingTimer = threading.Timer(self.SendingInterval,self.SendingAction)
        self.SendingTimer.start()      
        
    def stop(self):
        if(self.SendingClient != None):
            self.SendingClient.disconnect()
        if(self.ReceivingClient != None):
            self.ReceivingClient.loop_stop()
            self.ReceivingClient.disconnect()
        if(self.SendingTimer != None):
            self.SendingTimer.cancel()
        if(self.SelfTimer != None):
            self.SelfTimer.cancel()

    def SendingAction(self):
        if(self.IsSender):
            jsonString = self.createJSONString()
            print('To '+self.SendingTarget+':'+jsonString)
            self.SendingClient.publish(self.SendingTarget, jsonString)
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
        if(self.IsReceiver):
            self.ReceivingClient.subscribe(self.ID)

    def on_message(self,client, userdata, message):
        jsonString = message.payload.decode()
        #print(jsonString)
        content = json.loads(jsonString)
        print('From '+content['ID']+':'+str(content['VALUE'])+' '+content['TIME'])

    def createJSONString(self):
        data = self.getRandomNumber()
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        jsonString = '{"ID":"'+self.ID+'","VALUE":'+str(data)+',"BATTERY":'+str(self.Battery)+',"TIME":"'+time+'"}'
        return jsonString
