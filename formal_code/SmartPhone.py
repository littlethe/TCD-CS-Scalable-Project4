from Device import Device
import time

class SmartWatch(Device):
    SendingInterval = 2
    RandomMinimum = 10
    RandomMaximum = 50
    RandomIsInt   = False
    IsSender      = True
    IsReceiver    = True


a = SmartWatch('SP1','SW1')
#a.run()
a.runReceiving()
time.sleep(5)
a.runSending()
