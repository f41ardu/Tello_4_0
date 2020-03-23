from telloTelegram.telloTelegram import Telegram
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
telegram = Telegram()

#sequenze
sequence = 1
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

stick = telegram.setStickData(299,300,500,500,3)
print(stick)
print(bytes(stick))

if __name__ == '__main__':

# connect to tello
#    while isinstance(get, str):
#        get = myTello.udp_send(packet,tellohost,telloport)
#        if isinstance(get, str):
#            print(len(get))
#            print("AAAA:",get)
#            time.sleep(0.5)
# wait until we get conn_rec
#    while isinstance(get, bytes):
#        bb = myTello.udp_get()
#        print(type(bb))
#        print(bb.decode("latin-1",errors="ignore"))

# take off
    sequence = 1
    #packet_type_id, command_id, sequence, data=[]
    packet, _ = telegram.build(104, 84, sequence)
    print("Takeoff ", packet.hex())
    get = myTello.udp_send(packet,tellohost,telloport)
    time.sleep(10)
# land
    sequence = sequence + 1
    packet, _ = telegram.build(104, 85, sequence,[0,])
    print("Land ", packet.hex())
    get = myTello.udp_send(packet,tellohost,telloport)
    
#stick
    # land
    sequence = sequence + 1
    packet, _ = telegram.build(104, 85, sequence, stick)
    print("Land ", packet.hex())
    get = myTello.udp_send(packet,tellohost,telloport)