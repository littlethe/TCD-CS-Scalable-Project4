from Device import Device

class HeartBeatSensor(Device):
    TimerInterval = 2
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True
        
a = HeartBeatSensor('HB1')
a.run()
