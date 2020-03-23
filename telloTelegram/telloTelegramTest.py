import telloTelegram
from udp.udp import myUDP
import time

# tello adress 
tellohost = '192.168.10.1'
#tellohost = 'localhost'

# use for test/ require repeater.js 
#tellohost = 'localhost'

# telloport
telloport = 8889

# udp handle 
myTello = myUDP()

# telegram object 
telegram = telloTelegram.Telegram()

#response from tello
get = ""
#start sequence
tt = b'conn_req:xx'
packet = bytearray(tt)
#packet.extend(map(ord, tt))
print("tt :",packet)

# Bytearray allows modification
packet[len(packet)-2] = 0x96
packet[len(packet)-1] = 0x17

if __name__ == '__main__':
    
    #packet_type_id, command_id, sequence_number, data=[]
    command1, _ = telegram.build(104, 84, 484)
    print(command1)
#    print(command2)
    