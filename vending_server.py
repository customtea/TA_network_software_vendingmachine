import socket
import threading
from net.teaserver import TeaServer, TeaSession

from vending_item import BackYard, ShopItem

from logging import getLogger, StreamHandler, FileHandler, Formatter, INFO, ERROR, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

ch = StreamHandler()
ch.setLevel(INFO) 
ch_formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.addHandler(ch)

# fh = FileHandler('log/test.log')
# fh.setLevel(ERROR)
# fh_formatter = Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
# logger.addHandler(fh) 

thread_mutex = threading.Lock()

class VendingService(TeaSession):
    back_yard: BackYard
    def __init__(self, soc: socket, yard) -> None:
        super().__init__(soc)
        self.back_yard = yard
    
    def service(self):
        banner = \
r"""
 ____        ____   ___
|  _ \  __ _|  _ \ / _ \
| | | |/ _` | | | | | | |
| |_| | (_| | |_| | |_| |
|____/ \__, |____/ \___/
       |___/
"""
        self.print(banner)
        
        while True:
            self.print("====Menu List====")
            for item in self.back_yard.itemlist():
                self.print(f"{item.name:<20} : {item.price}", end="")
                if not item.is_avaliable(): 
                    self.print("<- Sold Out")
                else:
                    self.print()
            self.print("=================")
            self.print("Choose an Item")
            sel_name = self.keywait()
            print(sel_name)
            item = self.back_yard.search_by_name(sel_name)
            if not item is None:
                self.print(f"{sel_name} is Selected")
                self.print("Item is avaliable. Please put in Money")
                break
            else:
                self.print("Selected Item is NOT avilable. Please Try Again")
                continue
        
        while True:
            money = self.keywait()
            if not money.isdecimal():
                self.print("Invalid Money. Try Again")
                continue
            money = int(money)
            if not money >= item.price:
                self.print("Not Enough money. Try Again")
                continue
            with thread_mutex:
                item.sell()
                self.back_yard.earn(item.price)
            self.print("Purchase Complete")
            charge = money - item.price
            if charge > 0:
                self.print(f"Charge is {charge}")
            break
        
        self.close()
        



def main(port_number, item_filename):
    backyard = BackYard.loadfile(item_filename)
    TS = TeaServer(port_number, session_class=VendingService, session_args=[backyard])
    logger.info("Vending Server Start")
    try:
        TS.up()
    except KeyboardInterrupt:
        backyard.savefile(item_filename)


if __name__ == '__main__':
    main(50000, "./item.json")

