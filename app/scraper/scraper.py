import time
from typing import List, Union, Dict

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.scraper.models import Item


BASE_URL = "https://realtylink.org/en/properties~for-rent?uc=0"


class PageScraper:
    """
    Class for scraping pages
    """
    def __init__(self) -> None:
        self.options = Options()
        self.driver = webdriver.Chrome(options=self._add_options())
        self.action_chains = ActionChains(self.driver)

    def _add_options(self) -> Options:
        # self.options.add_argument("--headless")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/58.0.3029.110 Safari/537.3"
        )

        return self.options

    def get_all_items(self) -> List[str]:
        self.driver.get(BASE_URL)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "property-thumbnail-item"))
        )

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
                if len(links) == 60:
                    return links

            self.click_next_page()

    def click_next_page(self) -> None:
        pager = self.driver.find_element(By.CLASS_NAME, "pager")
        next_page_element = pager.find_element(By.CLASS_NAME, "next")
        if "inactive" not in next_page_element.get_attribute("class"):
            time.sleep(0.5)
            next_page_element.click()
            time.sleep(0.5)


class ItemScraper(PageScraper):
    """
    Class for scraping items
    """
    def parse_single_item_by_link(self, link: str) -> Item:
        self.driver.get(link)
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1 [data-id="PageTitle"]'))
        )

        address = self._get_address()
        region = ",".join(address.split(",")[-2:]).strip()

        return Item(
            link_to_ad=link,
            title=self._get_title(),
            region=region,
            address=address,
            price=self._get_price(),
            description=self._get_description(),
            date="recently",
            count_room=self._get_rooms(),
            size=self._get_size_sqft(),
            img_array=self._get_img_array(),
        )

    def _get_title(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR, 'h1 [data-id="PageTitle"]'
        ).text

    def _get_address(self) -> str:
        return self.driver.find_element(
            By.CSS_SELECTOR,
            'h2[itemprop="address"]'
        ).text

    def _get_price(self) -> str:
        return (
            self.driver.find_element(
                By.CSS_SELECTOR,
                "div.price-container > div.price.text-right > span:nth-child(6)",
            )
            .text.replace(
                ",", "."
            )
            .split(" ")[0]
        )

    def _get_description(self) -> Union[str, None]:
        try:
            description = self.driver.find_element(
                By.CSS_SELECTOR, "div.row.description-row > div > div:nth-child(2)"
            ).text
            return description
        except NoSuchElementException:
            return None

    def _get_rooms(self) -> Dict[str, int]:
        """
        Get the number of rooms
        """
        room_elements = self.driver.find_elements(
            By.CSS_SELECTOR, "div.col-lg-12.description > div.row.teaser > div"
        )
        rooms = {}
        for element in room_elements:
            if "cac" in element.get_attribute("class").split(" "):
                text = element.text.strip()
                if text:
                    rooms["bedrooms"] = int(text.split()[0])
            elif "sdb" in element.get_attribute("class").split(" "):
                text = element.text.strip()
                if text:
                    rooms["bathrooms"] = int(text.split()[0])
        return rooms

    def _get_size_sqft(self) -> str:
        """
        Get the size in square feet
        """
        return self.driver.find_element(
            By.CSS_SELECTOR,
            "div.col-lg-12.description > div:nth-child(6) > div:nth-child(1) > div.carac-value > span",
        ).text.replace(
            ",", "."
        )

    def _get_img_array(self) -> Union[List[str], None]:
        """
        Get the array of images
        """
        try:
            first_image = self.driver.find_element(
                By.CSS_SELECTOR, "div.primary-photo-container > a"
            )
            first_image.click()

            img_links = []

            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.description > strong"))
            )
            description = self.driver.find_element(
                By.CSS_SELECTOR, "div.description > strong"
            ).text
            total_images = int(description.split("/")[1])

            while len(img_links) < total_images:
                current_img = self.driver.find_element(
                    By.CSS_SELECTOR, 'img[src*="mediaserver.realtylink.org"]'
                )
                img_links.append(current_img.get_attribute("src"))
                self.action_chains.send_keys(Keys.ARROW_RIGHT).perform()

            return img_links
        except TimeoutException:
            return None
