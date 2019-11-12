from Device import Device

class HeartBeatSensor(Device):
    TimerInterval = 10
    RandomMinimum = 1
    RandomMaximum = 3
    RandomIsInt   = True
    IsSender      = True
        
a = HeartBeatSensor('HBM1')
a.run()