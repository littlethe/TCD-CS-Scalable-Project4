from Device import Device

class SmartWatch(Device):
    IsReceiver = True


a = SmartWatch('SW1')
a.run()
