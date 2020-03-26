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
        
# ping handle 
#ping = Ping(tellohost,1,2) # Ping(tellohost,1,2)
# udp handle 
myTello = myUDP()
# telegram handle
telegram = Telegram()


print ('\r\n\r\nTello r/c Control.\r\n')

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
            
        # Tell land       
        if button[0] == 0 and inAir == True:
            telegramData, telegramDatahex = telegram.land()
            print("Land ", telegramData)
            get = myTello.udp_send(telegramData,tellohost,telloport)           
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
myTello.close()
print ('quit ...')


 
