# ref: https://github.com/FreeOpcUa/python-opcua

import logging
import time
from camera import*
#import color
from color import*
from opcua import ua, uamethod, Server
#import ocr
import snap7
from bitstring import BitArray
import cv2
import numpy as np

plc_IP = '192.168.0.20'
DB = 2000
client = snap7.client.Client()
# ------------------------------------------------------------------------------

logging.basicConfig(level=logging.WARN)

# ------------------------------------------------------------------------------
#PLC Functions
# ------------------------------------------------------------------------------
#Read from PLC

def read_ready_load():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 4 (db_number,start, syze)
  B = BitArray(read)
  bit = B.bin[7]
  client.disconnect()
  #print 'read_load_done'
  #print bit
  return int(bit) 

def read_load_done():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 4 (db_number,start, syze)
  B = BitArray(read)
  bit = B.bin[6]
  client.disconnect()
  #print bit
  return int(bit)

def read_oven_cure_done ():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 2  
  B = BitArray(read)
  client.disconnect()
  bit = B.bin[5]
  #print num
  return int(bit)

def read_in_pos_turntable_load ():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads a byte
  B = BitArray(read)
  bit = B.bin[4]
  client.disconnect()
  #print bit
  return int(bit)

def read_in_pos_turntable_drill ():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads a byte 2
  B = BitArray(read)
  bit = B.bin[3]
  client.disconnect()
  #print bit
  return int(bit)

def read_drill_done():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 2
  B = BitArray(read)
  bit = B.bin[2]
  client.disconnect()
  #print bit
  return int(bit)

def read_in_pos_turntable_conveyor():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 2
  B = BitArray(read)
  bit = B.bin[1]
  client.disconnect()
  #print bit
  return int(bit)

def read_in_pos_unload():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,2,1)# reads byte 2
  B = BitArray(read)
  bit = B.bin[0]
  client.disconnect()
  #print bit
  return int(bit)

def read_unload_done():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,3,1)# reads byte 3
  B = BitArray(read)
  bit = B.bin[7]
  client.disconnect()
  #print bit
  return int(bit)

def read_framework_state():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,3,1)# reads byte 3
  B = BitArray(read)
  bit = B.bin[6]
  client.disconnect()
  #print bit
  return int(bit)

# Inspections
def color_inspect():
  try:
    #print("Estou aqui")
    img = capture_image(0,10)
    #cv2.imshow("p",img)
    #cv2.waitKey(0)
    #print("cenas")
    col = determine(img)
    #print("cenas1")
    #print("Estou aqui a dar a cor")
    return col
  except:
    print("Error capturing image!")
    return "Error"


def read_type():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,4,2)# reads byte 3
  client.disconnect()
  return read

# --------------------------------------
#Write to PLC

def start(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 0,state)# first bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def load(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 1,state)# second bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def oven_cure(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 2,state)# third bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def move_to_turntable(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 3,state)# fourth bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def move_turntable_to_drill(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 4,state)# fifth bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def drill(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 5,state)# sixth bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def move_turntable_to_conveyor(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 6,state)# seventh bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def move_to_unload(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,0,1)# reads byte 0
  snap7.util.set_bool(read, 0, 7,state)# eigth bit
  read = client.db_write(DB,0,read)
  client.disconnect()

def unload(state):
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,1,1)# reads byte 0
  snap7.util.set_bool(read, 0, 0,state)# first bit
  read = client.db_write(DB,1,read)
  client.disconnect()

def framework_activate():
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_read(DB,1,1)# reads byte 0
  snap7.util.set_bool(read, 0, 1,state)# second bit
  read = client.db_write(DB,1,read)
  client.disconnect()

def itype(color):
    return {
      'yellow': 4,
      'green': 2,
      'blue': 1,
      'purple': 3,
      'None': 0,
      'Error':0
      }[color]

def write_type(num):###
  client.connect(plc_IP,0,1) # rack and slot
  read = client.db_write(DB,4,bytearray([0,num]))
  client.disconnect()

# ------------------------------------------------------------------------------
#OPC methods
# ------------------------------------------------------------------------------

# PLC Readings
@uamethod
def plc_read_ready_load (parent):
  bit = read_ready_load()
  return bit 

@uamethod
def plc_read_load_done (parent):
  bit = read_load_done()
  return bit

@uamethod
def plc_read_oven_cure_done (parent):
  bit  = read_oven_cure_done()
  return bit 

@uamethod
def plc_read_in_pos_turntable_load (parent):
  bit = read_in_pos_turntable_load ()
  return bit

@uamethod
def plc_read_in_pos_turntable_drill(parent):
  bit = read_in_pos_turntable_drill()
  return bit 

@uamethod
def plc_read_drill_done(parent):
  bit =read_drill_done()
  return bit

@uamethod
def plc_read_in_pos_turntable_conveyor(parent):
  bit =read_in_pos_turntable_conveyor()
  return bit

@uamethod
def plc_read_in_pos_unload(parent):
  bit =read_in_pos_unload()
  return bit

@uamethod
def plc_read_unload_done(parent):
  bit =read_unload_done()
  return bit

@uamethod
def plc_read_framework_on(parent):
  bit = read_framework_state()
  return bit

#PLC writings  
@uamethod
def plc_start(parent,state):
  start(state)

@uamethod
def plc_load(parent,state):
  load(state)

@uamethod
def plc_oven_cure(parent,state):
   oven_cure(state)

@uamethod
def plc_move_to_turntable(parent, num):###
  move_to_turntable(num)

@uamethod
def plc_move_turntable_to_drill(parent, state):
  move_turntable_to_drill(state)

@uamethod
def plc_drill(parent, state):
  drill(state)
  
@uamethod
def plc_move_turntable_to_conveyor(parent, state):
  move_turntable_to_conveyor(state)

@uamethod
def plc_move_to_unload(parent, state):
  move_to_unload(state)

@uamethod
def plc_unload(parent, state):
  unload(state)

@uamethod
def plc_framework_on(parent, state):
  framework_activate(state)

#OCR inspection
@uamethod
def color_inspection(parent):
  result = color_inspect()
  return result

# ----------------------------------------------------------------------------------------------------------------------
#OPC Server
class AppServer(object):

  def __init__(self,
               endpoint="opc.tcp://192.168.0.200:12345/example/server/",
               uri="http://this.example.eu",
               name="Example"):

    # set up server
    self.server = Server()
    self.server.set_endpoint(endpoint)
    self.server.set_server_name(name)

    # set up namespace (optional)
    idx = self.server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = self.server.get_objects_node()

    # populating our address space
    obj_product = objects.add_object("ns={0};s=KIT".format(idx), "KIT")
    #self.var_digit = obj_product.add_variable("ns={0};s=KIT.digit".format(idx), "Digit", -1)
    self.var_color = obj_product.add_variable("ns={0};s=KIT.color".format(idx), "Color", "None")
    # CR Method
    ReadColor_node = obj_product.add_method("ns={0};s=KIT.color_inspect".format(idx), "Color Inspection", color_inspection,[], [ua.VariantType.Int16])

    #PLC methods
    #To Read

    plc_read_rload_node = obj_product.add_method("ns={0};s=KIT.plc_read_rload_done".format(idx), "Read Ready Load", plc_read_ready_load,[],[ua.VariantType.Boolean])
    plc_read_load_done_node = obj_product.add_method("ns={0};s=KIT.plc_read_load_done".format(idx), "Read Load done", plc_read_load_done,[],[ua.VariantType.Boolean])
    plc_read_ovenCure_done_node = obj_product.add_method("ns={0};s=KIT.plc_read_ovenCure_done".format(idx), "Read ovenCure done", plc_read_oven_cure_done,[],[ua.VariantType.Boolean])
    plc_read_inPos_turntable_load_node = obj_product.add_method("ns={0};s=KIT.plc_read_inPos_turntable_load".format(idx), "Read in position turntable", plc_read_in_pos_turntable_load,[],[ua.VariantType.Boolean])
    plc_read_inPos_turntable_drill_node = obj_product.add_method("ns={0};s=KIT.plc_read_inPos_turntable_drill".format(idx), "Read in_pos_turntable_drill", plc_read_in_pos_turntable_drill,[],[ua.VariantType.Boolean])
    plc_read_drill_done_node = obj_product.add_method("ns={0};s=KIT.plc_read_drill_done".format(idx), "Read drill_done", plc_read_drill_done,[],[ua.VariantType.Boolean])
    plc_read_inPos_turntable_conveyor_node = obj_product.add_method("ns={0};s=KIT.plc_read_inPos_turntable_conveyor".format(idx), "Read inPos_turntable_conveyor", plc_read_in_pos_turntable_conveyor,[],[ua.VariantType.Boolean])
    plc_read_inPos_unload_node = obj_product.add_method("ns={0};s=KIT.plc_read_inPos_unload".format(idx), "Read inPos_unload", plc_read_in_pos_unload,[],[ua.VariantType.Boolean])
    plc_read_unload_node = obj_product.add_method("ns={0};s=KIT.plc_read_unload".format(idx), "Read unload", plc_read_unload_done,[],[ua.VariantType.Boolean])

    #To Write
    plc_write_start_node = obj_product.add_method("ns={0};s=KIT.plc_write_start".format(idx), "Write start", plc_start,[ua.VariantType.Boolean], [])
    plc_write_load_node = obj_product.add_method("ns={0};s=KIT.plc_write_load".format(idx), "Write load", plc_load,[ua.VariantType.Boolean], [])
    plc_write_ovenCure_node = obj_product.add_method("ns={0};s=KIT.plc_write_oven_cure".format(idx), "Write Type", plc_oven_cure,[ua.VariantType.Int16], [])
    plc_write_move2turntable_node = obj_product.add_method("ns={0};s=KIT.plc_write_move2turntable".format(idx), "Write move turntable", plc_move_to_turntable,[ua.VariantType.Boolean], [])
    plc_write_mv_turntable2drill_node = obj_product.add_method("ns={0};s=KIT.plc_write_move_to_drill".format(idx), "Write move turntable to drill", plc_move_turntable_to_drill,[ua.VariantType.Boolean], [])
    plc_write_drill_node = obj_product.add_method("ns={0};s=KIT.plc_write_drill".format(idx), "Write drill", plc_drill,[ua.VariantType.Boolean], [])
    plc_write_mv_turntable2conveyor_node = obj_product.add_method("ns={0};s=KIT.plc_write_turntable2conveyor".format(idx), "Write move turntable to conveyor", plc_move_turntable_to_conveyor,[ua.VariantType.Boolean], [])
    plc_write_mv2unload_node = obj_product.add_method("ns={0};s=KIT.plc_write_move_to_unload".format(idx), "Write move to unload", plc_move_to_unload,[ua.VariantType.Boolean], [])
    plc_write_unload_node = obj_product.add_method("ns={0};s=KIT.plc_unload".format(idx), "Write unload", plc_unload,[ua.VariantType.Boolean], [])
    plc_write_framework_on_node = obj_product.add_method("ns={0};s=KIT.plc_write_framework_on".format(idx), "Write framework on", plc_framework_on,[ua.VariantType.Boolean], [])

  def start(self):

    self.server.start()

  def stop(self):

    self.server.stop()

  def set_color(self, color):

    self.var_color.set_value(color)

# ------------------------------------------------------------------------------
#Test unit
#-------------------------------------------------------------------------------

if __name__ == "__main__":
  
  srv = AppServer()
  srv.start()
  framework_ON = 0
  
  try:
    
    while True:
      framework_ON = read_framework_state() # checks if framework is connected
      if framework_ON == 0:
        print("framework OFF")
        if read_load_done() == 1:
          print("load is done")
          time.sleep(3)
          color = color_inspect()
          print(color)
          t = itype(color)
          if t >0 and t <5:
            write_type(t)
            time.sleep(0.2)
            #move conveyer          
        time.sleep(1)
  finally:
    srv.stop()
