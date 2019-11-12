from Device import Device

class BloodPressureSensor(Device):
    SendingInterval = 1
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True

class BreathSensor(Device):
    SendingInterval = 10
    RandomMinimum = 1
    RandomMaximum = 3
    RandomIsInt   = True
    IsSender      = True

class HeartBeatSensor(Device):
    SendingInterval = 2
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True

class SmartPhone(Device):
    SendingInterval = 2
    RandomMinimum = 10
    RandomMaximum = 50
    RandomIsInt   = False
    IsSender      = True
    IsReceiver    = True

class SmartWatch(Device):
    SendingInterval = 3
    RandomMinimum = 0
    RandomMaximum = 5
    RandomIsInt   = False
    IsSender      = True
    IsReceiver    = True

class BloodPressureSensor(Device):
    SendingInterval = 15
    RandomMinimum = 70
    RandomMaximum = 180
    RandomIsInt   = False
    IsSender      = True
