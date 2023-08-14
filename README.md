# Amazon Product Scraper

This repository contains a Scrapy spider specifically designed to scrape detailed product information from Amazon's website, focusing on `www.amazon.ae`.

## Features

- Retrieves extensive product details:
  - Title, Current price, Old price
  - Delivery options, Availability, ASIN
  - Seller rank, Number of reviews
  - Brand, Dimensions, Size, Batteries
  - Color, Weight

- Employs helper functions and Scrapy's `ItemLoader` to extract and clean scraped data.
- Uses the ScraperAPI service for bypassing rate limits and captchas. Replace 'xxxxxx' with your actual API key.
- Example configuration: Searches for "Iphone" products from page 1. Modifiable as needed.

## 📦 Dependencies

- [Scrapy](https://docs.scrapy.org/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [w3lib](https://github.com/scrapy/w3lib)

## 🚀 Usage

1. **Setup**:
   - Install the required packages:
     ```bash
     pip install scrapy pandas w3lib
     ```
   - Set your ScraperAPI key in place of 'xxxxxx' in the `API` variable.

2. **Run the Spider**:
   - From the project directory:
     ```bash
     scrapy crawl amazon
     ```

3. **Output**:
   - Data is saved to `amazon_SEARCHTERM.csv`, with `SEARCHTERM` being your chosen product (e.g., "Iphone").
   - The spider cleans the CSV post-run, removing empty columns.

## 💬 Contributing

Pull requests, feedback, and suggestions are welcome! For questions or issues, please open an issue.
