__author__ = 'Nick Sarris (ngs5st)'

import engine_lister
from scrapers import jewelry_scraper

def main():

    selling_category = "Jewelry"
    walmart_key = ""
    rescrape_data = False

    if rescrape_data != False:
        if selling_category == "Jewelry":
            jewelry_scraper.walmart_jewelry(walmart_key)
            jewelry_scraper.ebay_jewelry()
            jewelry_scraper.data_cleanup()

    engine_lister.list_ebay(selling_category)

if __name__ == '__main__':
    main()