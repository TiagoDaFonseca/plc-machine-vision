from modules.ocr import Inspection
from modules.server import App
from opcua import ua, uamethod

@uamethod
def inspect(parent):
    ipt = Inspection()
    number = ipt.read_number()
    return number

class ocrApp(App):
    def __init__(self):
        super().__init__()

        # add method 
        readnumber_node = self.product.add_method(self.ocr_space, "Inspection", inspect, [], [ua.VariantType.Int64])

if __name__ == "__main__":
    srv = ocrApp()