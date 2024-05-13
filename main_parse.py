import time
from dataclasses import dataclass, fields

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@dataclass
class Item:
    link_to_ad: str
    # title: str
    # region: str
    # address: str
    # description: str
    # img_array: list
    # date: str
    # price: float
    # count_room: int
    # size: float

