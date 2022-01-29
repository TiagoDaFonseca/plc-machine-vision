#
# THe idea is the connect shop floor elements with high level layers
# For that we add an intermediate component that acts as an OPC server
# and is able to receive requests and change PLC vaariable states.
#
#
#
###########################################################################

import plc
from modules.server import Server
from modules.ocr import Inspection
import time
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    pass