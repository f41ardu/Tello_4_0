import udp

host = '10.34.5.1'
port = 8889
if __name__ == '__main__':
    # new class object 
    u = udp.myUDP()
    
    # test loop 
    while True:
        try:
            # send something
            get = u.udp_send('command'.encode(encoding="utf-8"), host, port)
            # show response 
            print(get)
        except AttributeError:
            pass