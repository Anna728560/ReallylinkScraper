from dataclasses import dataclass


@dataclass
class Item:
    link_to_ad: str
    title: str
    region: str
    address: str
    description: str
    img_array: list
    date: str
    price: str
    count_room: dict
    size: str

    def to_dict(self):
        return {
            "link_to_ad": self.link_to_ad,
            "title": self.title,
            "region": self.region,
            "address": self.address,
            "description": self.description,
            "img_array": self.img_array,
            # 'date': self.date,
            "price": self.price,
            "count_room": self.count_room,
            "size": self.size,
        }
