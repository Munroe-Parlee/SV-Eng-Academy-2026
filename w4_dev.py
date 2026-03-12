#imports
import machine
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

class time:
    hh = 0
    mm = 0
    ss = 0



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
    
def trigger_alarm():
    while True:
        write('bang!!', 0)
        sleep(0.5)
        clear_screen()
        sleep(0.5)
    

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

##########==========button interface================######
def button_pressed():
    pass
##########==========joystick interface================######
def cursor_left():
    pass

def cursor_right():
    pass

def joystick_left():
    pass

def joystick_right():
    pass
##############servo interface====================##########
def get_servo_position():
    pass

def set_servo_position():
    pass

########=============audio interface============#########
def play_note():
    pass

def play_tune():
    pass
#========working code==========#
setup() 

rs.value(1) # select register 1 - necessary to send display input


string = 'hello world' #string of characters to be displayed
pause = 0.025
# while True:
#     write(string = string, pause = pause)
#     sleep(1)
#     clear_screen()
#     sleep(1)
#     countdown()
#     sleep(1)
#     write()
#     sleep(1)



#To comment or uncomment multiple lines of code, select the lines and press cmd+3
#comment in the next block of code and rerun your program

# clear_screen()
# utime.sleep_us(300000)
# string = 'alarm clock' # new string to display
# pause_length = 500000 #speed that characters appear
# for x in string: 	
#     send2LCD8(ord(x))	
#     utime.sleep_us(pause_length)

# #overflow time checking
# set_time(0, 59, 55)
# run_clock()

# #negative time checking
# set_time(-1, 59, 5)
# run_clock()

#alarm trigger checking

set_alarm(12, 0)
arm_alarm(True)
set_time(11, 59, 55)
run_clock()

# 
# 
# 
