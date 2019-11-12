from Device import Device
import time

class SmartWatch(Device):
    SendingInterval = 3
    RandomMinimum = 0
    RandomMaximum = 5
    RandomIsInt   = False
    IsSender      = True
    IsReceiver    = True

a = SmartWatch('SW1','SP1')
a.run()
