from opcua import ua, Server
from random import randint
import datetime 
import time 
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="App")


class App(Server):
    def __init__(self, 
                    endpoint="opc.tcp://127.0.0.1:4840/server/", 
                    uri="http://inspections.for.industry.com",
                    name="ocr server"):
        
        super().__init__()
        # set endpoint
        self.set_endpoint(endpoint)
        # give server a name
        self.set_server_name(name)
        # set up namespace (optional)
        self.ocr_space = self.register_namespace(uri)
        # get Objects node, this is where we should put our objects
        self.objects = self.get_objects_node()
        # populate our object nodes
        self.product = self.objects.add_object(self.ocr_space, "Product")
        # add variable to the object
        self.id = self.product.add_variable(self.ocr_space, "ID", -1)
        # set variable to be writable by client
        self.id.set_writable()

# TEST UNIT
if __name__ == "__main__":

    srv = App()
    srv.start()
    
    try:
        count = 0
        while count<10:
            time.sleep(1)
            count += 1
            srv.id.set_value(count)
            print(srv.id.get_value())
    finally:
        #close connection, remove subcsriptions, etc
        srv.stop()
        print("server stopped")