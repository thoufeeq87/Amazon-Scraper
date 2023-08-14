import scrapy
from ..items import AmazonProductItem
from scrapy.loader import ItemLoader
import pandas as pd

API = 'xxxxxx'  # This is a placeholder for our scraping service key.


def get_url(url):
    proxy_url = f'http://api.scraperapi.com/?api_key={API}&url={url}'
    return proxy_url


# Here's our main scraper for Amazon.
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.ae', 'api.scraperapi.com']
    search_term = "Iphone"  # What we're looking for on Amazon.
    page = 1  # We'll start from page 1.
    start_urls = [f'https://www.amazon.ae/s?k={search_term}&page={page}']

    # We start scraping from here.
    def parse(self, response):
        # Grabbing links of products on the current page.
        hrefs = [link.attrib['href'] for link in response.css("a[class*='s-link-style a-text-normal']")]
        base_url = "https://www.amazon.ae"

        for href in hrefs:
            href = base_url + href
            # Going to the product page to get more details.
            yield scrapy.Request(url=get_url(href), callback=self.parse_product, meta={'URL': href})
            # yield scrapy.Request(href, callback=self.parse_product, meta={'URL': href})

        # If there's a next page, let's scrape it too.
        nextpage = response.css(
            "div.a-section.a-text-center.s-pagination-container a.s-pagination-next::attr(href)").get()
        if nextpage:
            next_page_url = base_url + nextpage
            yield scrapy.Request(next_page_url, callback=self.parse)

    # This is where we pull details from each individual product page.
    def parse_product(self, response):
        weight_elements = response.css("th.prodDetSectionEntry:contains('Weight') + td.prodDetAttrValue")
        size_elements = response.css("table.a-bordered strong:contains('Size')")
        asin_elements = response.css("th.a-color-secondary a-size-base prodDetSectionEntry:contains('ASIN')")
        # Setting up a way to hold the details we're about to pull.
        item = ItemLoader(item=AmazonProductItem(), selector=response)
        # Here, we're pulling various details like title, price, reviews, etc.
        item.add_css("Title", "span[id='productTitle']")
        item.add_css("Current_Price", "span[class*='a-offscreen']")
        item.add_css("Old_Price", "span[class*='a-price a-text-price'] span")
        item.add_css("Delivery", "span[data-csa-c-delivery-price]::attr(data-csa-c-delivery-price)")
        item.add_css("Availability", "div[id ='availability']")
        item.add_css("Amazon_Seller_Rank", "span.a-list-item:contains('Best Sellers Rank')::text")
        item.add_value('URL', response.meta.get('URL', ''))
        if asin_elements:
            item.add_css("ASIN", "table[id='productDetails_detailBullets_sections1'] td[class*='prodDetAttrValue']")
        else:
            item.add_css("ASIN",
                         "th.prodDetSectionEntry:contains('ASIN') + td.prodDetAttrValue,div[id "
                         "='detailBullets_feature_div'] span :contains('ASIN') + span")
        item.add_css("Customer_Reviews", "span[data-hook='rating-out-of-text']")
        item.add_css("No_of_Reviews", "div[data-hook='total-review-count']")
        item.add_css("Brand", "th.prodDetSectionEntry:contains('Brand') + td.prodDetAttrValue")
        item.add_css("Dimension",
                     "th.prodDetSectionEntry:contains('Dimension') + td.prodDetAttrValue,div[id "
                     "='detailBullets_feature_div'] span :contains('Dimension') + span")
        if size_elements:
            item.add_css("Size", "table.a-bordered td:nth-child(2) p")
        item.add_css("Batteries",
                     "th.prodDetSectionEntry:contains('Battery') + td.prodDetAttrValue, "
                     "th.prodDetSectionEntry:contains('Batteries') + td.prodDetAttrValue")
        item.add_css("Color", "th.prodDetSectionEntry:contains('Color') + td.prodDetAttrValue")

        if weight_elements:
            item.add_css("Weight", "th.prodDetSectionEntry:contains('Weight') + td.prodDetAttrValue")
        else:
            item.add_css("Total_Weight",
                         "th.prodDetSectionEntry:contains('Dimension') + td.prodDetAttrValue, div[id "
                         "='detailBullets_feature_div'] span :contains('Dimension') + span")
        # Once we've got everything, hand it off.
        yield item.load_item()

    # Once we're done scraping everything...
    def close(self, reason):
        # We're cleaning up our scraped data and saving it.
        df = pd.read_csv(f'amazon_{self.search_term}.csv')
        df = df.dropna(axis=1, how='all')  # Removing any empty columns.
        df.to_csv(f'amazon_{self.search_term}.csv', index=False)
