#
# Tello Python3 r/c Controll 
#
# (c) 02/2020 f41ardu 
#
# MIT Lisence
'''
https://www.heise.de/forum/heise-online/News-Kommentare/Nutzerandrang-Dienste-von-Microsoft-365-werden-eingeschraenkt/Eine-Cloud-sie-zu-knechten/posting-36372321/show/

Eine Cloud sie zu knechten
Drei Wolken als ClickDummy und ab in das Licht,
Sieben dem Marketing mit ihren Hirnen voll Koks,
Den Sterblichen, ewig dem Fenster verfallen, neun,

Eine dem lustigen Onkel auf seinem Thron,
Im Lande CloudAlle, wo die Einschränkungen drohn.
Eine Wolke, sie zu knechten, sie alle zu finden,
Ins Kuckucksheim zu treiben und ewig zu binden

Im Lande CloudAlle, wo die Dummheit erhält ihren Lohn.
'''

import pygame
import time
import math

from udp.udp import myUDP
from telloTelegram.telloTelegram import Telegram
from telloTelegram.telloFlightData import FlightData
 

# Define some colors
darkgrey = (40, 40, 40)
lightgrey = (150, 150, 150)

# Tello variables 
inAir = False
button = [0,0,0,0,0,]
axisTello = [0,0,0,0,0,0,0,0,0,]

# tello adress 
tellohost = '192.168.10.1'

# use for test/ require repeater.js 
#tellohost = 'localhost'

# telloport
telloport = 8889

# RC control variables
RC_VAL_MID = 1024
fast       = 0 # not used 
thr        = RC_VAL_MID
yaw        = RC_VAL_MID
pitch      = RC_VAL_MID
roll       = RC_VAL_MID 

# low-level Protocol (https://tellopilots.com/wiki/protocol/#MessageIDs)
START_OF_PACKET                     = 0xcc
SSID_MSG                            = 0x0011
SSID_CMD                            = 0x0012
SSID_PASSWORD_MSG                   = 0x0013
SSID_PASSWORD_CMD                   = 0x0014
WIFI_REGION_MSG                     = 0x0015
WIFI_REGION_CMD                     = 0x0016
WIFI_MSG                            = 0x001a
VIDEO_ENCODER_RATE_CMD              = 0x0020
VIDEO_DYN_ADJ_RATE_CMD              = 0x0021
EIS_CMD                             = 0x0024
VIDEO_START_CMD                     = 0x0025
VIDEO_RATE_QUERY                    = 0x0028
TAKE_PICTURE_COMMAND                = 0x0030
VIDEO_MODE_CMD                      = 0x0031
VIDEO_RECORD_CMD                    = 0x0032
EXPOSURE_CMD                        = 0x0034
LIGHT_MSG                           = 0x0035
JPEG_QUALITY_MSG                    = 0x0037
ERROR_1_MSG                         = 0x0043
ERROR_2_MSG                         = 0x0044
VERSION_MSG                         = 0x0045
TIME_CMD                            = 0x0046
ACTIVATION_TIME_MSG                 = 0x0047
LOADER_VERSION_MSG                  = 0x0049
STICK_CMD                           = 0x0050
TAKEOFF_CMD                         = 0x0054
LAND_CMD                            = 0x0055
FLIGHT_MSG                          = 0x0056
SET_ALT_LIMIT_CMD                   = 0x0058
FLIP_CMD                            = 0x005c
THROW_AND_GO_CMD                    = 0x005d
PALM_LAND_CMD                       = 0x005e
TELLO_CMD_FILE_SIZE                 = 0x0062  # pt50
TELLO_CMD_FILE_DATA                 = 0x0063  # pt50
TELLO_CMD_FILE_COMPLETE             = 0x0064  # pt48
SMART_VIDEO_CMD                     = 0x0080
SMART_VIDEO_STATUS_MSG              = 0x0081
LOG_HEADER_MSG                      = 0x1050
LOG_DATA_MSG                        = 0x1051
LOG_CONFIG_MSG                      = 0x1052
BOUNCE_CMD                          = 0x1053
CALIBRATE_CMD                       = 0x1054
LOW_BAT_THRESHOLD_CMD               = 0x1055
ALT_LIMIT_MSG                       = 0x1056
LOW_BAT_THRESHOLD_MSG               = 0x1057
ATT_LIMIT_CMD                       = 0x1058 # Stated incorrectly by Wiki (checked from raw packets)
ATT_LIMIT_MSG                       = 0x1059

# Connection state
Connected = False

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
 
    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, lightgrey)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
       
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
       
    def indent(self):
        self.x += 10
       
    def unindent(self):
        self.x -= 10
        
def byte_to_hexstring(buf):
    if isinstance(buf, str):
        return ''.join(["%02x " % ord(x) for x in buf]).strip()

    return ''.join(["%02x " % ord(chr(x)) for x in buf]).strip() 
 
# udp handle 
myTello = myUDP()
# telegram object
telegram = Telegram()
# flightdata object
flightdata = FlightData()

print ('\r\n\r\nTello r/c Control.\r\n')
tt = b'\xcc\x18\x01\xb9\x88V\x00c\x05\x00\x00\x01\x00\xff\xff\x00\x00\xaf\x03\x00\x00Q\x00\x000\x0f\x00\x06\x00\x00\x00\x00\x00\xef\xcc'
flight_data = flightdata.getData(tt[9:])
print(flight_data)


# launch pygame panel 
pygame.init()
# connect 
telegramData, telegramDatahex = telegram.connect()
print("Connect ", telegramData)
get = myTello.udp_send(telegramData,tellohost,telloport)
# connect to tello
while isinstance(get, str):
    get = myTello.udp_send(telegramData,tellohost,telloport)
    print(len(get))
    print("AAAA:",get)
    time.sleep(0.5)

bb = myTello.udp_get()
print(type(bb))
conn = bb.decode("latin-1",errors="ignore")
if not 'conn_ack' in conn: 
    conn = bb.decode("latin-1",errors="ignore")
else:
    conntected = True

getBack=myTello.udp_get()
cmd = int.from_bytes(getBack[5:6], "little")
if cmd == WIFI_MSG:
    print('Recived WIFI Message: ',getBack)


# Set the width and height of the screen [width,height]
size = [500,500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("R/C Tello")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
   
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
           
    # DRAWING STEP
    # First, clear the screen to darkgrey. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(darkgrey)
    textPrint.reset()
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
 
    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    # print("Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    getBack=myTello.udp_get()
    cmd = int.from_bytes(getBack[5:6], "little")
    #cmd = (getBack[5] & 0xff) | ((getBack[6] & 0xff) << 8)
    #if cmd == WIFI_MSG:
    #    print('Recived WIFI Message: ',getBack)
    #    print("recv: wifi: %s" % byte_to_hexstring(getBack[9:]))
    #if cmd == LOW_BAT_THRESHOLD_MSG:
    #    print("recv: low battery threshold: %s" % byte_to_hexstring(getBack[9:-2]))
    #if cmd == FLIGHT_MSG:
    #    flight_data = flightdata.getData(getBack[9:])
    #    print(flight_data)
    if cmd == LOG_HEADER_MSG:
        flight_data = flightdata.getData(getBack[9:])
        print("log_header:",flight_data)
    if cmd == LOG_DATA_MSG:
        flight_data = flightdata.getData(getBack[9:])
        print("log_data:",flight_data)   
    if cmd == LOG_CONFIG_MSG:
        flight_data = flightdata.getData(getBack[9:])
        print("log_config:",flight_data)   
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
   
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
   
        # read controller buttons 
        # buttons is controller specific / check your buttons befor your first fligth
        # assignment is like sticks depending from controller used, check before first flight
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()
 
        # read all buttons avalabel 
        for i in range( buttons ):
            button[i] = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button[i]) )
            reading = button[0]
            
        # Tello take off    
        if button[0] == 1 and inAir == False:
            # take off
            telegramData, telegramDatahex = telegram.takeoff()
            print("takekoff:",telegramData)
            get = myTello.udp_send(telegramData,tellohost,telloport)
            time.sleep(0.05)
            inAir = True
            
        # Tello land       
        if button[0] == 0 and inAir == True:
            telegramData, telegramDatahex = telegram.land()
            print("Land ", telegramData)
            get = myTello.udp_send(telegramData,tellohost,telloport)
            time.sleep(0.05)
            inAir=False
            
   # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        # get axis and assign to controll channels
        # assignmemt and magic number 1600 is controller dependend, check your controller
        #
        # input range for .stick is from -1000 to 1000 
        for i in range( axes ):
            axisTello[i] = int(1600*joystick.get_axis( i ))
            textPrint.print(screen, "Axis {} value: {:>6.0f}".format(i, axisTello[i]) )
        textPrint.unindent()
        fast  = 0 # not used
        pitch = -axisTello[2] # move left / right
        roll  =  axisTello[0] # move forward / backward
        thr   = -axisTello[1] # move up / down
        yaw   =  axisTello[4] # turn left/right
        
        # if Airborne send channels 
        if inAir:
            #                                       .stick(fast, roll, pitch, thr, yaw)
            telegramData, telegramDatahex = telegram.stick(fast, roll, pitch, thr, yaw)
            myTello.udp_send(telegramData,tellohost,telloport)
                     
        textPrint.unindent()
#        textPrint.unindent()
        
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
   
    # Go ahead and update the screen with what we've drawn.
    # this is not the Tello flip command!
    pygame.display.update()
 
    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.

pygame.quit ()
myTello.udp_close()
print ('quit ...')


 
