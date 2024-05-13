from dataclasses import fields

from app.scraper.scraper import WebScraperService, Item
from app.writter.writter import CSVFileWriter


ITEM_FIELDS = [field.name for field in fields(Item)]


def get_all_items():
    scraper = WebScraperService()
    all_items = []
    links = scraper.get_all_items()
    for link in links:
        item = scraper.parse_single_item_by_link(link)
        all_items.append(item)

    return all_items


if __name__ == "__main__":
    items = get_all_items()
    file_writer = CSVFileWriter(file_name="app_items", column_fields=ITEM_FIELDS)
    file_writer.write_in_csv_file(data=items)
