#imports
import machine
import utime

#interface definition
rs = machine.Pin(16,machine.Pin.OUT) 	#rs: 	register select
e = machine.Pin(17,machine.Pin.OUT)		#e: 	enable/disable changes
d4 = machine.Pin(18,machine.Pin.OUT)	#d4-7: 	sends binary information through pins i.e. serial output
d5 = machine.Pin(19,machine.Pin.OUT)
d6 = machine.Pin(20,machine.Pin.OUT)
d7 = machine.Pin(21,machine.Pin.OUT)

#=========functions definition=========#
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
    
def clear_screen():
    rs.value(0)		#select command register
    send2LCD8(0x01) #clear screen
    rs.value(1)		#select input register
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

#========working code==========#
setUpLCD() 

rs.value(1) # select register 1 - necessary to send display input


string = 'hello world' #string of characters to be displayed

#for loop which will display the string of characters on string
for x in string: 	# runs the indented code once per character in the string surrounded by ''
    send2LCD8(ord(x))	#sends an instruction to display the next character in the string
    utime.sleep_us(300000)	#sleep time in micro seconds i.e. wait for 40 micro seconds between displaying characters

#To comment or uncomment multiple lines of code, select the lines and press cmd+3
#comment in the next block of code and rerun your program

# clear_screen()
# utime.sleep_us(300000)
# string = 'alarm clock' # new string to display
# pause_length = 500000 #speed that characters appear
# for x in string: 	
#     send2LCD8(ord(x))	
#     utime.sleep_us(pause_length)

#try changing the pause_length and string variables from the last code block



