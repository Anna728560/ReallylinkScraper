import time
from dataclasses import dataclass

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@dataclass
class Item:
    link_to_ad: str
    title: str
    region: str
    address: str
    description: str
    # img_array: list
    # date: str
    price: str
    count_room: dict
    size: str


class WebScraperService:
    BASE_URL = "https://realtylink.org/en/properties~for-rent?uc=0"

    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self._add_options())

    def _add_options(self) -> Options:
        # self.options.add_argument("--headless")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )

        return self.options

    def get_all_items(self):
        self.driver.get(self.BASE_URL)
        time.sleep(2)

        links = []

        while True:
            item_elements = self.driver.find_elements(
                By.CLASS_NAME, "property-thumbnail-item"
            )
            for item_element in item_elements:
                link_to_ad = item_element.find_element(By.TAG_NAME, "a").get_attribute(
                    "href"
                )
                links.append(link_to_ad)
                # if len(links) == 30:
                if len(links) == 5:
                    return links

            self.click_next_page()

    def click_next_page(self):
        pager = self.driver.find_element(By.CLASS_NAME, "pager")
        next_page_element = pager.find_element(By.CLASS_NAME, "next")
        if "inactive" not in next_page_element.get_attribute("class"):
            time.sleep(1)
            next_page_element.click()
            time.sleep(1)

    def parse_single_item_by_link(self, link):
        self.driver.get(link)
        time.sleep(2)

        address = self._get_address()
        region = address.split(",")[-1]

        return Item(
            link_to_ad=link,
            title=self._get_title(),
            region=region,
            address=address,
            price=self._get_price(),
            description=self._get_description(),
            # img_array=self._get_img_array(),
            count_room=self._get_rooms(),
            size=self._get_size_sqft(),
        )

    def _get_title(self):
        return self.driver.find_element(
            By.CSS_SELECTOR, 'h1 [data-id="PageTitle"]'
        ).text

    def _get_address(self):
        return self.driver.find_element(By.CSS_SELECTOR, 'h2[itemprop="address"]').text

    def _get_price(self):
        return (
            self.driver.find_element(
                By.CSS_SELECTOR,
                "div.price-container > div.price.text-right > span:nth-child(6)",
            )
            .text.replace("$", "")
            .replace(",", ".")
            .split(" ")[0]
        )

    def _get_description(self):
        try:
            description = self.driver.find_element(
                By.CSS_SELECTOR, "div.row.description-row > div > div:nth-child(2)"
            ).text
            return description
        except NoSuchElementException:
            return None

    def _get_rooms(self):
        room_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "div.col-lg-12.description > div.row.teaser > div"
        )
        rooms = {}
        for element in room_elements:
            if "cac" in element.get_attribute("class").split(" "):
                rooms["bedrooms"] = int(element.text.split()[0])
            elif "sdb" in element.get_attribute("class").split(" "):
                rooms["bathrooms"] = int(element.text.split()[0])
        return rooms

    def _get_size_sqft(self):
        return self.driver.find_element(
            By.CSS_SELECTOR,
            "div.col-lg-12.description > div:nth-child(6) > div:nth-child(1) > div.carac-value > span",
        ).text

    def _get_img_array(self):
        first_image = self.driver.find_element(
            By.CSS_SELECTOR, "div.primary-photo-container > a"
        )
        first_image.click()

        img_links = []

        description = self.driver.find_element(
            By.CSS_SELECTOR, "div.description > strong"
        ).text
        total_images = int(description.split("/")[1])

        current_img = self.driver.find_element(
            By.CSS_SELECTOR, 'img[src*="mediaserver.realtylink.org"]'
        )
        img_links.append(current_img.get_attribute("src"))

        while len(img_links) < total_images:
            pass

        return img_links