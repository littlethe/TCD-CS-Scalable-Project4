from Device import Device

class BloodPressureSensor(Device):
    SendingInterval = 15
    RandomMinimum = 70
    RandomMaximum = 180
    RandomIsInt   = False
    IsSender      = True
        
a = BloodPressureSensor('BP1','SW1')
a.run()
