import typing
import json


def json_encode_item(o):
    if isinstance(o, ShopItem):
        return o.__dict__
    raise TypeError(repr(o) + " is not JSON serializable")


class ShopItem():
    def __init__(self, itemid, itemname: str, price: int, stock: int, sold: int) -> None:
        self.iid = itemid
        self.name = itemname
        self.price = price
        self.stock = stock
        self.sold = sold
    
    def addstock(self, count) -> None:
        self.stock += count
    
    def is_avaliable(self) -> bool:
        return self.stock > 0
    
    def sell(self) -> None:
        self.stock -= 1
        self.sold += 1
    
    @classmethod
    def load_dict(cls, keyid, d):
        return cls(keyid, d["name"], int(d["price"]), int(d["stock"]), int(d["sold"]))


class BackYard():
    __storage: typing.Dict[str, ShopItem] = {}
    __profit = 0
    def __init__(self, item_dict) -> None:
        for key, value in item_dict.items():
            self.__storage[key] = ShopItem.load_dict(key, value)
        self.__profit = 0
    
    def earn(self, value):
        self.__profit += value
    
    
    def search_by_name(self, name) -> typing.Union[ShopItem, None]:
        for iid, item in self.__storage.items():
            if item.name == name:
                return item
        return None
    
    def itemlist(self):
        return list(self.__storage.values())
    
    @classmethod
    def loadfile(cls, filename):
        with open(filename, "r") as f:
            item_dict = json.load(f)
            return cls(item_dict)

    def savefile(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__storage, f, default=json_encode_item, indent=4)

