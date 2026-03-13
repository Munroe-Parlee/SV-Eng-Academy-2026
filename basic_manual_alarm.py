#imports
import machine
from machine import Pin,PWM,ADC
import utime
# import text
# from hardware_tutorial import clear_screen, register_select, issue_hardware_command, setup, sleep
#interface definition
rs = machine.Pin(16,machine.Pin.OUT) 	#rs: 	register select
e = machine.Pin(17,machine.Pin.OUT)		#e: 	enable/disable changes
d4 = machine.Pin(18,machine.Pin.OUT)	#d4-7: 	sends binary information through pins i.e. serial output
d5 = machine.Pin(19,machine.Pin.OUT)
d6 = machine.Pin(20,machine.Pin.OUT)
d7 = machine.Pin(21,machine.Pin.OUT)

#=========functions definition=========#

#========reference information===========#
#=display command information=#
#Sr.No.		Hex Code	Command to LCD instruction Register
#1			01			Clear display screen
#2			02			Return home
#3			04			Decrement cursor (shift cursor to left)
#4			06			Increment cursor (shift cursor to right)
#5			05			Shift display right
#6			07			Shift display left
#7			08			Display off, cursor off
#8			0A			Display off, cursor on
#9			0C			Display on, cursor off
#10			0E			Display on, cursor blinking
#11			0F			Display on, cursor blinking
#12			10			Shift cursor position to left
#13			14			Shift the cursor position to the right
#14			18			Shift the entire display to the left
#15			1C			Shift the entire display to the right
#16			80			Force cursor to the beginning ( 1st line)
#17			C0			Force cursor to the beginning ( 2nd line)
#18			38			2 lines and 5×7 matrix

#registers:
    # register 0: command input
    # register 1: letter and digit input
    
    #=============================pin interface========================#
rs = machine.Pin(16,machine.Pin.OUT) 	#rs: 	defines register select pin
e = machine.Pin(17,machine.Pin.OUT)		#e: 	defines pin for enable/disable changes signal
d4 = machine.Pin(18,machine.Pin.OUT)	#d4-7: 	defines serial output pins
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
    
def send2LCD8(BinNum): # #sends an instruction to display a character in a string
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

    #=============================hardware interface========================#
    
def setUpLCD():				#sets up display
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

def register_select(register):
    rs.value(register)
    
def issue_hardware_command(hexcode):
    register_select(0)
    send2LCD8(hexcode)
    register_select(1)
    
def clear_screen():
    rs.value(0)		#select command register
    send2LCD8(0x01) #clear screen
    rs.value(1)		#select input register

def setup():			#initialises program
    setUpLCD()
    issue_hardware_command(0x01)
    
def sleep(seconds=0.5): #default sleep time is 0.25s
    nanoseconds = int(1000000 * seconds)
    utime.sleep_us(nanoseconds)
    
    #=============================display interface========================#
def display_string(string = "helloWrld", pause = 0):
        #for loop which will display the string of characters on string
    for x in string: 	# runs the indented code once per character in the string surrounded by " "
        sleep(pause)	#sleep time in micro seconds i.e. wait for 40 micro seconds between displaying characters
        display_character(x)
    pass

def display_character(x = "A"):
    send2LCD8(ord(x))	#sends an instruction to display a character
    pass

def write(string = "          ", pause = 0):
    clear_screen()
    sleep(0.05)
    display_string(string, pause)
    
    #=============================clock interface========================#
# class time:
#global time variables
hh = 0
mm = 0
ss = 0

alarm_string = "00:00:00"
alarm_set = False
alarm_trigger = False
alarm_armed = False

# class time:
#     hh = 0
#     mm = 0 
#     ss = 0



run_clock = False
def display_time(hours = 0, minutes = 0, seconds = 0):
    time = time_string(hours, minutes, seconds)
    
    write(f"{time}", pause = 0)
    return time
    pass

def time_string(hours = 0, minutes = 0, seconds = 0):
    time = f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"
    return time
    pass

def set_time(hours = 0, minutes = 0, seconds = 0):
    global hh
    global mm
    global ss
    if hours < 0:
        hours = 0
    if minutes < 0:
        minutes = 0
    if hours < 0:
        hours = 0
    hh = hours
    mm = minutes
    ss = seconds
    display_time(hh, mm, ss)
    pass


def run_clock():
    global alarm_trigger
    global run_clock
    run_clock = True
    
    while run_clock is True:
        sleep(1)
        tick()
        if alarm_armed is True:
            check_alarm()
            if alarm_trigger is True:
                trigger_alarm()
        

def tick():
    global hh
    global mm
    global ss
    display_time(hh, mm, ss)
#     while seconds > 59 or minutes > 59:
#         if seconds > 59:
#             minutes += 1
#             seconds -= 60
#         if minutes > 59:
#             hours += 1
#             minutes -= 60
    ss += 1
    if ss > 59:
        ss = 0
        mm += 1
    
    if mm > 59:
        mm = 0
        hh += 1
   
    if hh > 23:
       hh = 0
        
    
    display_time(hh, mm, ss)
    pass

def countdown(seconds=3):
    register_select(1)
    remaining_time = seconds
    
    for x in range(seconds+1):
#         reset_display()
        sleep(0.5)
        display_time(0, 0, seconds-x)
        sleep(0.5)
    sleep(0.5)    
    write(string = 'bang!!', pause = 0.005)
    sleep(0.5)

####===========alarm interface========#####
    

    

def arm_alarm(flag):
    global alarm_armed
    alarm_armed = flag
    pass

def check_alarm():
    global alarm_trigger
    global alarm_string
    global alarm_set
    global alarm_armed
    global run_clock
    global hh
    global mm
    
    if alarm_armed is True:
        if time_string(hh, mm) == alarm_string:
            trigger_alarm()
            run_clock = False
    pass

def set_alarm(hours = 0, minutes = 0):
    global alarm_string
    global alarm_trigger
    global alarm_set
    global alarm_armed
    
    alarm_string = time_string(hours, minutes)
    alarm_trigger = False
    alarm_set = True
    alarm_armed = True
    write(f"alarm set: {alarm_string}")
    sleep(1)
    pass
####################======================input interfaces======================###############
##########==========input backend===================######

##########==========button interface================######
#button pin definition
button = Pin(1,Pin.IN,Pin.PULL_DOWN)
state = 0
def check_button():
    if button.value() == 1:
        return True
    else:
        return False
    pass

def button_pressed():
    #add button event code here
    increment_state()
    pass

def increment_state():
    global state
    state += 1
##########==========joystick interface================######
def move_cursor_left():
#     issue_hardware_command(04)
    pass

def cursor_right():
    pass

def joystick():
    value = get_joystick_position()
    if value<45:
        joystick_left()
    if value > 135:
        joystick_right()
    sleep(0.5)
def joystick_left():
    decrement_time()
    pass

def joystick_right():
    increment_time()
    pass

def decrement_time():
    global hh
    global mm
    global ss
    global state
    if state == 0:
        set_time(hours = hh-1, minutes = mm, seconds = ss)
    if state == 1:
        set_time(hours = hh, minutes = mm -1, seconds = ss)
    if state == 2:
        set_time(hours = hh, minutes = mm, seconds = ss -1)
    pass

def increment_time():
    global hh
    global mm
    global ss
    global state
    if state == 0:
        set_time(hours = hh+1, minutes = mm, seconds = ss)
    if state == 1:
        set_time(hours = hh, minutes = mm+1, seconds = ss)
    if state == 2:
        set_time(hours = hh, minutes = mm, seconds = ss+1)
    pass
##############servo interface====================##########
# servo = PWM(Pin(0))#Include the servo motor pin
# joyX = ADC(28)#Include the potentiometer pin
# servo.freq(50)#Set the frequency
# speaker = machine.Pin(5, Pin.OUT)

#PWM min and max value
joyX = ADC(27)#Include the potentiometer pin

in_min = 0
in_max = 65535
#Servo motor min and max degrees
out_min = 1000
out_max = 9000

def get_joystick_position():
    global in_min
    global in_max
    #Servo motor min and max degrees
    global out_min
    global out_max
    value = joyX.read_u16()
    position = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return position

def set_servo_position():
    pass
####misc####

from time import sleep

servo = PWM(Pin(0))#Include the servo motor pin
joyX = ADC(26)#Include the potentiometer pin

#servo frequency definition 
servo.freq(50)#Set the frequency

#speaker pin definition
speaker = machine.Pin(5, Pin.OUT)

@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    in_shiftdir=rp2.PIO.SHIFT_LEFT,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
)

def wave_prog():
    pull(block)
    mov(x, osr)         # waveCount
    pull(block)
    label("loop")
    mov(y, osr)         # halfWaveNumCycles
    set(pins, 1)        # high
    label("high")
    jmp(y_dec, "high")
    mov(y, osr)         # halfWaveNumCycles
    set(pins, 0)        # low
    label("low")
    jmp(y_dec, "low")
    jmp(x_dec, "loop")
    
# the clock frequency of Raspberry Pi Pico is 125MHz; 1953125 is 125MHz / 64
sm = rp2.StateMachine(0, wave_prog, freq=1953125, set_base=Pin(5)) 
sm.active(1)
########=============audio interface============#########
def play_note(freq: int, duration: int):
    # count 1 cycle for jmp() ==> 1 cycle per half wave ==> 2 cycles per wave
    halfWaveNumCycles = round(1953125.0 / freq / 2)
    waveCount = round(duration * freq / 1000.0)
    sm.put(waveCount)
    sm.put(halfWaveNumCycles)
    pass

def play_tune():
    pass
#========working code==========#
setup() 

rs.value(1) # select register 1 - necessary to send display input

############edit this to change alarm behaviour##################
def trigger_alarm():
    while True:
        write('bang!!', 0)
        sleep(0.5)
        clear_screen()
        sleep(0.5)
#####################write user code here#######################

###manual
set_time(11, 59, 55)
set_alarm(12, 0)
run_clock()
