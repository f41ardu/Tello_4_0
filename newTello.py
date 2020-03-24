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


print(telegram.connect()) 

telegramData = telegram.stick(299,300,500,500,3)
#print(stick)

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
    telegramData, telegramDatahex = telegram.takeoff()
    print("takekoff:",telegramData)
    get = myTello.udp_send(telegramData,tellohost,telloport)
    time.sleep(1)
# land
    telegramData, telegramDatahex = telegram.land()
    print("Land ", telegramData)
    get = myTello.udp_send(telegramData,tellohost,telloport)
    
