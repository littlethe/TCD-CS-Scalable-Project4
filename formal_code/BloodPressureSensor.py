from Device import Device

class BloodPressureSensor(Device):
    SendingInterval = 1
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True
        
a = BloodPressureSensor('BP1','SW1')
a.run()
