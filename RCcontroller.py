#
# Tello Python3 r/c Controll 
#
# (c) 02/2020 f41ardu 
#
# MIT Lisence

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
#tellohost = '192.168.10.1'

# use for test/ require repeater.js 
tellohost = 'localhost'

# telloport
telloport = 8889

# RC control variables 
a = 0
b = 0
c = 0
d = 0

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

# connect 
telegramData, telegramDatahex = telegram.connect()
print("Connect ", telegramData)
get = myTello.udp_send(telegramData,tellohost,telloport)   

print ('\r\n\r\nTello r/c Control.\r\n')

# Establish connection ( is Tello available
#while (not Connected):
#    Connected = ping.ping(tellohost,1,1)
#    print('Connected: ', Connected)

# when Tello is available set Tello into command mode
#Connected = False
#while (not Connected):
#    get = u.udp_send('command',tellohost,telloport) 
#    if get == 'ok':
#        Connected = True
#        print('Tello in Command mode: ', Connected)
# launch pygame panel 
pygame.init()
 
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
   
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
       
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        # the magic number 160 is controller dependend, check your controller 
        for i in range( axes ):
            axisTello[i] = int(160*joystick.get_axis( i ))
            textPrint.print(screen, "Axis {} value: {:>6.0f}".format(i, axisTello[i]) )
        # a,b,c,d depends from your controller / check stick assignemt before 
        textPrint.unindent()
        a = axisTello[0]
        b = -axisTello[2]
        c = -axisTello[1]
        d = axisTello[4]
        msg = "rc " + str(a) + " " + str(b) + " " + str(c) + " " + str(d)
        if inAir and math.sqrt(a*a+b*b+c*c+d*d) > 5:
            telegramData, telegramDatahex = telegram.stick(fast, roll, pitch, thr, yaw)
            myTello.udp_send(telegramData,tellohost,telloport)
        
        # axis2 = forward/backward  b
        # axis2 = left / reight a
        # axis1 = up/down d
        #axis4 = yaw c
        # buttons depend from your controller / check buttons first
        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()
 
        for i in range( buttons ):
            button[i] = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button[i]) )
            reading = button[0]
        # take off    
        if button[0] == 1 and inAir == False:
            # take off
            telegramData, telegramDatahex = telegram.takeoff()
            print("takekoff:",telegramData)
            get = myTello.udp_send(telegramData,tellohost,telloport)
            time.sleep(0.05)
            inAir = True
        # landing       
        if button[0] == 0 and inAir == True:
            telegramData, telegramDatahex = telegram.land()
            print("Land ", telegramData)
            get = myTello.udp_send(telegramData,tellohost,telloport)           
            inAir=False
    
        textPrint.unindent()
        textPrint.unindent()
        
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
print ('quit ...')
myTello.close() 


 