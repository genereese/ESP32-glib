
# Handle imports
from machine import Pin, ADC

import shared


class Battery:

    def __init__(self, pin=4, voltage_min=3.2, voltage_max=4.2, voltage_charge=4.2):

        # Configure the ADC pin
        self._voltage = ADC(Pin(pin))
        self._voltage.atten(ADC.ATTN_11DB)

        # Configure the attributes
        self.voltage_min = voltage_min
        self.voltage_max = voltage_max
        self.voltage_range = voltage_max - voltage_min
        self.voltage_charge = voltage_charge

        self.voltage_display = self.getVoltage()
    
    def getVoltage(self):
        
        return (self._voltage.read_uv() / 1000000) * 2

    def getVoltageString(self):

        return f"{self.getVoltage():.2f}" + "V"
    
    def getPercent(self):
        
        percentage = round((((self.voltage_range - (self.voltage_max - self.getVoltage())) / self.voltage_range) * 100), 1)
        return shared.clamp(percentage, 0, 100)

    def getPercentString(self):

        return str(int(self.getPercent())) + "%"

    def read(self):
        
        return round((self._voltage.read_uv() / 1000000) * 2, 2)


class Joystick:

    def __init__(self, pin_x, pin_y, deadzone_min=1985, deadzone_max=2000):

        # Configure the axis ADC pins        
        self._axis_x = ADC(Pin(pin_x))
        self._axis_y = ADC(Pin(pin_y))

        # Attenuate the ADC pins
        self._axis_x.atten(ADC.ATTN_11DB)
        self._axis_y.atten(ADC.ATTN_11DB)

        # Set the attributes
        self.axis_min = 0
        self.axis_max = 4095
        self.deadzone_min = deadzone_min
        self.deadzone_max = deadzone_max
    
    def _mapToPercent(self, value, percent=100):

        # Map value to percentage
        if (value > self.deadzone_max):
            return int(((value - self.deadzone_max) / (self.axis_max - self.deadzone_max)) * percent)
        elif (value < self.deadzone_min):
            return -int(((value - self.deadzone_min) / (self.deadzone_min - self.axis_min)) * -percent)
        else:
            return 0
    
    def read(self):

        percent_x = self._mapToPercent(self._axis_x.read())
        percent_y = self._mapToPercent(self._axis_y.read())

        return percent_x, percent_y


