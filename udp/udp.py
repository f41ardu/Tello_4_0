#
# --- send/receive thread for communication over udp
#     (c)2020 f41ardu
#     MIT lisence
# 
from threading import Thread
import socket, time

class myUDP(object):
    """
    A class used to implement an udp socket using threading

    ...

    Attributes
    ----------
    addr : str
        a formatted with IP or DNS / Hostname
    port : int
        the port number listening to
        
    Methods
    -------
    myUDP (addr='0.0.0.0', port=9000, dgram=1518)
        # create listner on listner port and ipadress and dgram length
        # default values: IP: 0.0.0.0 and port 9000
    udp_deamon(self)
        # Read the next frame from the stream in a different thread by using threading
    udp_send((self, data='', targetAddr='localhost', targetPort=8889)    
        # send already encoded data to target adress using target port
    udp_close(self)
       # close udp listner
    """
    
    def __init__(self, addr='0.0.0.0', port=9000, dgram=2048):
        """
        The udp instance myUDP
        
        Parameters
        -----------
        addr : str
        a formatted with IP or DNS / Hostname (default = '0.0.0.0')
        port : int
        the port number listening to (default = 9000)
        dgram : int 
        the dgram to be send (default = 2048)
        Returns
        -------
        An upd object with methods
        """
        src = (addr,port)
        
        if dgram > 2**16:
            dgram = 2**16
            
        self.MAX_DGRAM = dgram
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(src)
        self.received =''
        #self.data_rec = bytearray(1024)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.__upd_deamon, args=())
        self.thread.daemon = True
        self.thread.start()
                    

    def __upd_deamon(self):
        """
        The listner: Read the next frame from the stream in a different thread
        Prameters
        ---------
            None - private method
        Returns
        -------
            None
        """
        while True:
            
            self.received, self.addr = self.sock.recvfrom(self.MAX_DGRAM)
            #self.received = self.seg
    def udp_get(self):
        return self.received
    
    def udp_send(self, data='', targetAddr='localhost', targetPort=8889):
        """ Send data via udp to target host
        
        Parameters
        ----------
        data: str
            The data sent to the target
        targetAddr: str
            The target host, optional, see default
        targetPort: ind
            the target port, optional, see default
        Returns:
            Response data from target
        """
        print (data, targetAddr, targetPort)
        #sent=self.sock.sendto(data.encode(encoding="utf-8"),(targetAddr, targetPort))
        sent=self.sock.sendto(data,(targetAddr, targetPort))
        print (sent)
        #print("A:",self.data_rec)
        return self.received
     
    def upd_close(self):
        """ Close udp connection
        
        Parameters
        ----------
            None
        Returns
        -------
            None
        """
        print('udp close....')
        #sent=self.sock.sendto('close'.encode(encoding="utf-8"),(targetAddr, targetPort))
        self.sock.close()
