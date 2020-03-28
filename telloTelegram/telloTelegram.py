# simple class to build data telegrams for Tello
"""
document me
"""
import datetime
from . import crc

class Telegram():
   
    def __init__(self):
        self.start=b'\xcc'
        self.head = 11
        self.data = []
        self.sequence_number = 1

    def connect(self):
        tt = b'conn_req:xx'
        packet = bytearray(tt)
        # Bytearray allows modification
        packet[len(packet)-2] = 0x96
        packet[len(packet)-1] = 0x17
        return packet, packet.hex()
    
    def takeoff(self):
        self.sequence_number = self.sequence_number + 1 
        packet = self.build(104, 84, self.sequence_number)
        return packet, packet.hex()
    
    def land(self):
        self.sequence_number = self.sequence_number + 1
        packet = self.build(104, 85, self.sequence_number, [0,])
        return packet, packet.hex()
    
    def stick(self, fast, roll, pitch, thr, yaw):
        self.sequence_number = self.sequence_number + 1
        fast  = self._map(fast, -1000, 1000, 364, 1684)
        roll  = self._map(roll, -1000, 1000, 364, 1684)
        pitch = self._map(pitch, -1000, 1000, 364, 1684)
        thr   = self._map(thr, -1000, 1000, 364, 1684)
        yaw   = self._map(yaw, -1000, 1000, 364, 1684)
        # print(fast,roll,pitch,thr,yaw)
        # build data from stick input 
        self._setStickData(fast, roll, pitch, thr, yaw)
        # build and return package
        packet = self.build(96, 80, self.sequence_number, self.data)
        return packet, packet.hex()
        
    def build(self,packet_type_id, command_id, sequence_number, data=[]):
        # build the package
        # int to bytes 
        data = bytes(data)
        # all the magic here, I guess more or less self explaining 
        packet_type_id = packet_type_id.to_bytes(1, 'little')
        packet_size = (len(data) * 8 + self.head * 8).to_bytes(2, 'little')
        crc8 = crc.calcCRC8(self.start + packet_size, len(self.start + packet_size)).to_bytes(1, 'little')
        command_id = command_id.to_bytes(2, 'little')
        sequence_number = sequence_number.to_bytes(2, 'little')
        # concatenate 
        command = self.start + packet_size + crc8 + packet_type_id + command_id + sequence_number + data
        cLen = len(command)
        crc16 = crc.calcCRC16(command, cLen).to_bytes(2, 'little')
        # concatenate
        command = self.start + packet_size + crc8 + packet_type_id + command_id + sequence_number + data + crc16
        # return package
        return command

    def _setStickData(self,fast, roll, pitch, thr, yaw):
        now = datetime.datetime.now()
        stickData = (fast << 44) | (yaw << 33) | (thr << 22) | (pitch << 11) | (roll)
        self.data = [ 0xff & stickData, stickData >> 8 & 0xff,
                 stickData >> 16 & 0xff, stickData >> 24 & 0xff,
                 stickData >> 32 & 0xff, stickData >> 40 & 0xff,
                 now.hour, now.minute, now.second,
                 now.microsecond & 0xff, now.microsecond >> 16]
        self.sequence_number = 0
        return

    def _map(self ,x, in_min, in_max, out_min,  out_max):
        '''
        map value x in range in_min to in_max to out_min to out_max
        and restrict from MIN to MAX
        '''
        RC_VAL_MIN     = 364
        RC_VAL_MAX     = 1684
        map = int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
        if map < RC_VAL_MIN:
            map = 364
        if map >=1648:
            map = 1648
        return map

