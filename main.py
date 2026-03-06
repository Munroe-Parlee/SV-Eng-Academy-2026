import machine
import utime

rs = machine.Pin(16,machine.Pin.OUT)
e = machine.Pin(17,machine.Pin.OUT)
d4 = machine.Pin(18,machine.Pin.OUT)
d5 = machine.Pin(19,machine.Pin.OUT)
d6 = machine.Pin(20,machine.Pin.OUT)
d7 = machine.Pin(21,machine.Pin.OUT)

def pulseE():
    e.value(1)
    utime.sleep_us(40)
    e.value(0)
    utime.sleep_us(40)
def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >>4)
    d5.value((BinNum & 0b00100000) >>5)
    d6.value((BinNum & 0b01000000) >>6)
    d7.value((BinNum & 0b10000000) >>7)
    pulseE()
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0010)
    send2LCD8(0b00101000)
    send2LCD8(0b00001100)
    send2LCD8(0b00000110)
    send2LCD8(0b00000001)
    utime.sleep_ms(2)

setUpLCD()

for i in range(5): 
    for x in '12:1%dpm'%i:
        rs.value(1)
        send2LCD8(ord(x))
        utime.sleep_us(40)
    utime.sleep_ms(1000)

    rs.value(0)
    send2LCD8(0x01)
    utime.sleep_ms(2)


    


    