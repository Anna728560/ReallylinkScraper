# RealtlylinkScraper

Reallylink Scraper is a web scraping tool built in Python using Selenium. It is designed to scrape real estate data from the Reallylink website.

## Installation

1. Clone the repository:

   ```bash
    git clone https://github.com/Anna728560/RealtlylinkScraper.git
   ```

2. Install the required dependencies:

   ```bash
    pip install -r requirements.txt
   ```

## Usage

To scrape real estate data from Reallylink, run the `main_parse.py` script:

   ```bash
      python main_parse.py
   ```

## Result 

The result will be a list of 60 advertisements. Each advertisement is a separate object in a JSON file.

Example:

```
[
   {
     "link_to_ad": "https://reallylink.com/123",
     "title": "House for rent",
     "region": "West End VW, Vancouver",
     "address": "111 1540 Haro Street, West End VW, Vancouver",
     "description": "This beautiful house features...",
     "img_array": ["https://reallylink.com/image1.jpg", "https://reallylink.com/image2.jpg"],
     "data": "recently"
     "price": "$250,000",
     "count_room": {"bedrooms": 3, "bathrooms": 2},
     "size": "2000 sqft"
    },
    ...
]
```