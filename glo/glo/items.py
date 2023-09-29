import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_currency(value):
    #     KES28,000,000
    return value.replace('KES', '')

def remove_commas(value):
    value = remove_currency(value)
    return value.replace(',', '')

def try_float(value):
    try:
        return float(value)
    except ValueError:
        return value
    
def extract_location(value):
    #2,3 and 4 Bedroom Apartment For Sale In Kileleshwa, get Kileleshwa
    return value.split(' ')[-1]

def extract_service_type(value):
    #2,3 and 4 Bedroom Apartment For Sale In Kileleshwa, get For Sale
    return value.split(' ')[-3]





class GloItem(scrapy.Item):
    house_href = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    
    house_price = scrapy.Field(
        input_processor=MapCompose(remove_tags,remove_commas, try_float),
        output_processor=TakeFirst()
    )
    bed_rooms = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, int),
        output_processor=TakeFirst()
    )
    
    house_location = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, extract_location),
        output_processor=TakeFirst()
    )

    service_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, extract_service_type),
        output_processor=TakeFirst()
    )

