import snap7
from snap7.client import Client
from bitstring import BitArray
from modules.ocr import Inspection
import logging
import time

logger = logging.getLogger(name="plc")
logging.basicConfig(level=logging.WARN)

class PlcController(Client):
    def __init__(self, address='192.168.0.20', db=2000, rack=0, slot=1):
        super().__init__()
        self.ip_address = address
        self.db = db
        try:
            self.connect_to(rack, slot)
            logger.info(f"plc connected to {address}")
        except Exception as e:
            logger.error("Plc connection error.")
    
    def connect_to(self, rack, slot):
        self.connect(self.ip_address, rack, slot)

    # Reading Tasks if loading is available and if the load is done
    # When the load is done we are ready to perform inspection.
    # and  take decisions 
    def read_ready_load(self):
        read = self.db_read(self.db,2,1)# reads byte 4 (db_number,start, syze)
        B = BitArray(read)
        bit = B.bin[7]
        return int(bit) 
    
    def load(self, state):
        read = self.db_read(self.db,0,1)# reads byte 0
        snap7.util.set_bool(read, 0, 1, state)# second bit
        read = self.db_write(self.db,0, read)
    
    def read_load_done(self):
        read = self.db_read(self.db,2,1)# reads byte 4 (db_number,start, syze)
        B = BitArray(read)
        bit = B.bin[6]
        return int(bit)
    
    def write_type(self, num):###
        read = self.db_write(self.db,4,bytearray([0,num]))


if __name__ == "__main__":

    plc = PlcController()
    
    while(True):
        if plc.read_load_done() == 1:
            ipt = Inspection()
            num = ipt.read_number()
            if 0 <= num <= 5:
                plc.write_type(num)
        time.sleep(1)




    

