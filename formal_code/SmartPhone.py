from Device import Device
import time

class SmartPhone(Device):
    SendingInterval = 2
    RandomMinimum = 10
    RandomMaximum = 50
    RandomIsInt   = False
    IsSender      = True
    IsReceiver    = True


a = SmartPhone('SP1','SW1')
a.run()
