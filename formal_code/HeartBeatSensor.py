from Device import Device

class HeartBeatSensor(Device):
    SendingInterval = 2
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True
        
a = HeartBeatSensor('HB1','SW1')
a.run()
