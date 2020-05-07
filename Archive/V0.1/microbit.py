from bluezero import microbit
import constants

class MicrobitControl():
    
    def __init__(self):
        self.connect()

    def connect(self):
        self.ubit = microbit.Microbit(adapter_addr='B8:27:EB:74:98:54',
                         device_addr='CD:46:C2:B2:15:3B',
                         accelerometer_service=True,
                         button_service=True,
                         led_service=True,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=True)
        self.ubit.connect()

    def download(self):
        self.ubit.pixels = [0b00100, 0b00100, 0b10101, 0b01010, 0b00100] 

    def blank(self):
        self.ubit.pixels = [0b00000, 0b00000, 0b00000, 0b00000, 0b00000] 
    
    def noTraffic(self):
        self.ubit.pixels = [0b11011, 0b11011, 0b00000, 0b10001, 0b01110] 

    def trafficBuilding(self):
        self.ubit.pixels = [0b11011, 0b11011, 0b00000, 0b11111, 0b00000] 

    def trafficBad(self):
        self.ubit.pixels = [0b11011, 0b11011, 0b10000, 0b00100, 0b00001] 

    def trafficAwful(self):
        self.ubit.pixels = [0b11011, 0b11011, 0b00000, 0b01110, 0b10001] 

    def worstTraffic(self):
        self.ubit.pixels = [0b10001, 0b01010, 0b00000, 0b01110, 0b10001] 