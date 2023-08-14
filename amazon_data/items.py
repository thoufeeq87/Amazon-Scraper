import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
import unicodedata


# This function removes any "left-to-right mark" (or LRM) characters.
def remove_lrm(prod):
    return ''.join(c for c in prod if unicodedata.category(c) != 'Cf')


# This function strips out the currency notation "AED" (Arab Emirates Dirham).
def remove_cur(cur):
    return cur.replace("AED", "")


# This function tries to convert the price string into a float rounded to 3 decimal places.
# If it can't, it simply returns the original string.
def convert_float(price):
    try:
        return round(float(price), 3)
    except ValueError:
        return price


# This function extracts the part of the weight string before the ";" character.
def remove_weight(weight):
    return weight.split(";")[0]


# This function grabs everything after the ";" character in the weight string.
def extract_weight(weight):
    return weight.split(";")[1:]


# This function removes any opening bracket "(" from the provided text.
def remove_bracket(text):
    return text.replace("(", "")


# This is a definition for a Scrapy item to store Amazon product details.
class AmazonProductItem(scrapy.Item):
    # Each field corresponds to some attribute of the product on Amazon.
    # The product's title.
    Title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # The current price of the product.
    Current_Price = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_cur, convert_float),
        output_processor=TakeFirst()
    )
    # The original price if the product is on sale.
    Old_Price = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_cur, convert_float),
        output_processor=TakeFirst()
    )
    # Delivery details, Is it Free or cost.
    Delivery = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # Availability status like "in stock".
    Availability = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # ASIN is the Amazon Standard Identification Number.
    ASIN = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # The product's URL.
    URL = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # The product's rank in Amazon's bestseller list.
    Amazon_Seller_Rank = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_bracket),
        output_processor=TakeFirst()
    )
    # The average rating given by users.
    Customer_Reviews = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # Total number of reviews for the product.
    No_of_Reviews = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    # The brand of the product.
    Brand = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm),
        output_processor=TakeFirst()
    )
    # The product's dimension.
    Dimension = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm, remove_weight),
        output_processor=TakeFirst()
    )
    # The size details of the product.
    Size = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm),
        output_processor=TakeFirst()
    )
    # Battery details is Battery included or not.
    Batteries = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm),
        output_processor=TakeFirst()
    )
    # The color of the product.
    Color = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm),
        output_processor=TakeFirst()
    )
    # Weight of the product.
    Weight = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm),
        output_processor=TakeFirst()
    )
    #  Product's Weight, extracted from the dimension data.
    Total_Weight = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_lrm, extract_weight),
        output_processor=TakeFirst()
    )
