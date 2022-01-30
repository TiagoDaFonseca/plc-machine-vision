# ref: https://github.com/FreeOpcUa/python-opcua

import logging
import time

from opcua import ua, uamethod, Server
import ocr
import snap7
from bitstring import BitArray
# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.WARN)

# ------------------------------------------------------------------------------
#PLC readings
@uamethod
def plc_read_load (parent):
  plc = snap7.connect('171.20.20.10',0,1) # plc  nrack and slot
  read = plc.db_read(2000,0,1)# reads byte 0
  B = BitArray(read)
  bit = B.bin[7]
  plc.disconnect()
  return bit 

@uamethod
def plc_read_type (parent):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,2,2)# reads byte 2  
  num = BitArray(read).int
  plc.disconnect()
  return num

@uamethod
def plc_read_move_to_press (parent):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,0,1)# reads a byte
  B = BitArray(read)
  bit = B.bin[7]
  plc.disconnect()
  return bit 

@uamethod
def plc_read_move_to_unload(parent):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4
  B = BitArray(read)
  bit = B.bin[7]
  plc.disconnect()
  return bit 

@uamethod
def plc_read_unload(parent):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4 (db_number,start, syze)
  B = BitArray(read)
  bit = B.bin[6]
  plc.disconnect()
  return bit 

@uamethod
def plc_read_openmos_on(parent):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4
  B = BitArray(read)
  bit = B.bin[5]
  plc.disconnect()
  return bit
  
#PLC writings  
@uamethod
def plc_write_load(parent,state):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 0,state)#first bit
  read = plc.db_write(2000,0,1,read)
  #read = plc.db_write(read,2000,0,1)
  plc.disconnect()

@uamethod
def plc_write_move_to_press(parent,state):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 1,state)# second bit
  read = plc.db_write(2000,0,1,read)
  plc.disconnect()

@uamethod
def plc_write_type(parent, num):###
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_write(2000,2,2,BitArray(num))
  plc.disconnect()

@uamethod
def plc_write_move_to_unload(parent, state):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4
  snap7.util.set_bool(read, 0, 0,state) #first bit
  read = plc.db_write(2000,4,1,read)
  plc.disconnect()

@uamethod
def plc_write_unload(parent, state):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4
  snap7.util.set_bool(read, 0, 1,state) #second bit
  read = plc.db_write(2000,4,1,read)
  plc.disconnect()
  
@uamethod
def plc_write_openmos_on(parent, state):
  plc = snap7.connect('171.20.20.10',0,1) # rack and slot
  read = plc.db_read(2000,4,1)# reads byte 4
  snap7.util.set_bool(read, 0, 2,state) # third bit
  read = plc.db_write(2000,4,1,read)
  plc.disconnect()
  
#OCR inspection
@uamethod
def Inspect(parent, call):
  if call == True:
    #Connect camera 
    cam = ocr.connect_to_camera()
  
    #Check if is opened
    if not cam.isOpened():
      print("<<< Error Message: Camera not OK. Trying to open...")
      try:
        cam.open()
        print("Camera opened")
      except:
        print("<<< Error connecting")
  
    try:  
    #Reading number
      n = ocr.read_number(cam)
    #Outputs number
      print("number:" + n)
      cam.release()
      return n
    except:
      print("<<< Error Message: Reading number failure")
      print("")#new line
      return -1
  else:
      return -2

class AppServer(object):

  def __init__(self,
               endpoint="opc.tcp://0.0.0.0:4840/learning-kits/server/",
               uri="http://learning-kits.introsys.eu",
               name="Learning kits"):

    # set up server
    self.server = Server()
    self.server.set_endpoint(endpoint)
    self.server.set_server_name(name)

    # set up namespace (optional)
    idx = self.server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = self.server.get_objects_node()

    # populating our address space
    obj_product = objects.add_object(idx, "Product")
    self.var_digit = obj_product.add_variable(idx, "Digit", -1)
    
    # OCR Method
    ReadNumber_node = obj_product.add_method(idx, "Inspection", Inspect,[ua.VariantType.Boolean], [ua.VariantType.Int64])

    #PLC methods
    #To Read
    plc_read_load_node = obj_product.add_method(idx, "Read Load", plc_read_load,[],[ua.VariantType.Boolean])
    plc_read_type_node = obj_product.add_method(idx, "Read Type", plc_read_type,[], [ua.VariantType.Int64])
    plc_read_Mv2Press_node = obj_product.add_method(idx, "Read Mv2Press", plc_read_move_to_press,[], [ua.VariantType.Boolean])
    plc_read_Mv2Unload_node = obj_product.add_method(idx, "Read Mv2Unload", plc_read_move_to_unload,[], [ua.VariantType.Boolean])
    plc_read_unload_node = obj_product.add_method(idx, "Read Unload", plc_read_unload,[], [ua.VariantType.Boolean])
    plc_read_openmos_node = obj_product.add_method(idx, "Read OpenMOS ON", plc_read_openmos_on,[], [ua.VariantType.Boolean])

    #To Write
    plc_write_load_node = obj_product.add_method(idx, "Write Load", plc_write_load,[ua.VariantType.Boolean], [])
    plc_write_Mv2Press_node = obj_product.add_method(idx, "Write Mv2Press", plc_write_move_to_press,[ua.VariantType.Boolean], [])
    plc_write_type_node = obj_product.add_method(idx, "Write Type", plc_write_type,[ua.VariantType.Int64], [])
    plc_write_unload_node = obj_product.add_method(idx, "Write Unload", plc_write_unload,[ua.VariantType.Boolean], [])
    plc_write_Mv2Unload_node = obj_product.add_method(idx, "Write Mv2Unload", plc_write_move_to_unload,[ua.VariantType.Boolean], [])
    plc_write_openmos_node = obj_product.add_method(idx, "Write OpenMOS ON", plc_write_openmos_on,[ua.VariantType.Boolean], [])
    
    
  def start(self):

    self.server.start()

  def stop(self):

    self.server.stop()

  def set_digit(self, digit):

    self.var_digit.set_value(digit)

# ------------------------------------------------------------------------------
#Test unit
#-------------------------------------------------------------------------------

if __name__ == "__main__":
  
  srv = AppServer()
  srv.start()
  number = 0
  try:
    
    while True:
      
      number = 9
      srv.set_digit(number)
      time.sleep(1)
  finally:
    srv.stop()
