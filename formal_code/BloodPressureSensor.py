from Device import Device

class BloodPressureSensor(Device):
    TimerInterval = 10
    RandomMinimum = 80
    RandomMaximum = 120
    RandomIsInt   = True
    IsSender      = True
        
a = BloodPressureSensor('BP1')
a.run()
