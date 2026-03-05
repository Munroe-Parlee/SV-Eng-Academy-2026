from machine import Pin,PWM,ADC
from time import sleep

servo = PWM(Pin(0))#Include the servo motor pin
joyX = ADC(28)#Include the potentiometer pin
servo.freq(50)#Set the frequency
speaker = machine.Pin(5, Pin.OUT)

#PWM min and max value
in_min = 0
in_max = 65535
#Servo motor min and max degrees
out_min = 1000
out_max = 9000


while True:
    #Get the potentiometer values
    speaker.on()
    value = joyX.read_u16()
    
    #Convert PWM values from 0 to 180
    Servo = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    #Rotate the servo motor
    servo.duty_u16(int(Servo))
