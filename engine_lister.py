__author__ = 'Nick Sarris (ngs5st)'

import re
import time
import pandas as pd
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

def decide_category(item_name):

    category_dict = {

        "Anklet":                     101437,
        "Bracelet":       {"Diamond": 10976,
                           "Pearl":   164316,
                           "Other":   164315},
        "Earrings":       {"Diamond": 10986,
                           "Pearl":   10990,
                           "Other":   164321},
        "Necklace":       {"Diamond": 164331,
                           "Pearl":   164333,
                           "Other":   164332},
        "Pendant":        {"Diamond": 164331,
                           "Pearl":   164333,
                           "Other":   164332},
        "Brooch":         {"Pearl":   11013,
                           "Other":   164337},
        "Ring":           {"Diamond": 67726,
                           "Pearl":   11021,
                           "Other":   164343},
        "Band":           {"Diamond": 67726,
                           "Pearl":   11021,
                           "Other":   164343},
        "Other":                      505

    }

    category_list_1 = ["Diamond", "Pearl"]
    category_list_2 = ["Pearl"]

    for key in category_dict.keys():
        if key in item_name:
            if key not in ["Anklet", "Brooch"]:
                for cat in category_list_1:
                    if cat in item_name:
                        return cat, category_dict[key][cat]
                    else:
                        return "Other Gemstone", category_dict[key]["Other"]
            else:
                if key == "Brooch":
                    for cat in category_list_2:
                        if cat in item_name:
                            return cat, category_dict[key][cat]
                        else:
                            return "Other Gemstone", category_dict[key]["Other"]
                else:
                    return "Other Gemstone", category_dict[key]
        else:
            continue

    return "Other Gemstone", category_dict["Other"]

def list_ebay(selling_category):

    if selling_category == 'Jewelry':

        merchandise = pd.read_csv('data/jewelry_final.csv', encoding='ISO-8859-1')
        api = Trading(config_file='data/ebay_auth.yaml')

        counter = 0
        for i, row in merchandise.iterrows():
            while True:

                try:
                    print("Listing Item #{}: {}".format(i, row['name']))

                    item_name = row['name']
                    image_urls = row['images'].split(',')
                    description = row['long_description']
                    sale_price = ((int(row['sale_price']) * 1.15) - 0.01)
                    type, category = decide_category(row['name'])
                    upc_value = row['upc']

                    replacement_list = ["T.G.W.","T.W.","T.G.W","T.W","Created",
                                        "Princess-Cut","Cross-Over","Three Stone",
                                        "Cultured","Freshwater","Cocktail",
                                        "Three-Stone","Two-Tone"]

                    listing_title = re.sub(r' \d+\-\d+\/\d+ Carat', "", item_name)
                    listing_title = re.sub(r' \d+\/\d+ Carat', "", listing_title)
                    listing_title = re.sub(r' \d+\/\d+ CT', "", listing_title)
                    listing_title = re.sub(r' \d+\/\d+', "", listing_title)
                    listing_title = re.sub(r' \d+ Carat', "", listing_title)
                    listing_title = re.sub(r' \d+kt', "", listing_title)
                    listing_title = re.sub(r' \d+\-\d+\.\dmm', "", listing_title)
                    listing_title = re.sub(r' \d+\.\d+\-\d+\.\dmm', "", listing_title)
                    listing_title = re.sub(r' \d+\.\d+\-\dmm', "", listing_title)
                    listing_title = re.sub(r' \d+\-\dmm', "", listing_title)
                    listing_title = re.sub(r' \dmm+\-\d+\.\dmm', "", listing_title)
                    listing_title = re.sub(r' \d+\.\dmm+\-\d+\.\dmm', "", listing_title)
                    listing_title = re.sub(r' \d+\.\dmm+\-\dmm', "", listing_title)
                    listing_title = re.sub(r' \dmm+\-\dmm', "", listing_title)

                    for replacement in replacement_list:
                        listing_title = listing_title.replace(" " + replacement, "")

                    try:
                        listing_title = listing_title.split(',')[0]
                    except:
                        pass

                    if len(listing_title) < 80:

                        image_list = []
                        for image_url in image_urls:
                            image_url = image_url.replace('[','').replace(']','') \
                                                 .replace("'",'').split('?')[0].strip()
                            list.append(image_list, image_url)

                        myitem = {

                            "Item":{

                                "Title": listing_title,
                                "Description": '<![CDATA[<h3 style="color: inherit; font-family: inherit; background-color: '
                                               'rgb(255, 255, 255); box-sizing: border-box; line-height: 1.1; margin-top: 20px; '
                                               'margin-bottom: 20px; font-size: 24px;">'+ item_name +'</h3><hr><font rwr="1" '
                                               'size="4" style="font-family:Arial"><div><h3 style="color: inherit; font-family: inherit; '
                                               'background-color: rgb(255, 255, 255); box-sizing: border-box; font-weight: 500; '
                                               'line-height: 1.1; margin-top: 20px; margin-bottom: 10px; font-size: 24px;">Description</h3>'
                                               '<h3 style="color: inherit; font-family: inherit; background-color: rgb(255, 255, 255); '
                                               'box-sizing: border-box; font-weight: 500; line-height: 1.1; margin-top: 20px; '
                                               'margin-bottom: 10px; font-size: 24px;"><div><div style="font-family: Arial; '
                                               'font-size: 14pt;"><ul style="box-sizing: border-box; margin-top: 0px; '
                                               'margin-bottom: 10px; color: rgb(51, 51, 51); font-family: &quot;Helvetica Neue&quot;, '
                                               'Helvetica, Arial, sans-serif; font-size: medium;"><li style="box-sizing: border-box;">'
                                               'Gender: Women</li><li style="box-sizing: border-box;">Fine Or Fashion: Fine</li>'
                                               '<li style="box-sizing: border-box;">Brand: Miabella</li><li style="box-sizing: border-box;">'
                                               'Age Group: Adult</li><li style="box-sizing: border-box;">Gemstone Type: ' + type + '</li>'
                                               '<li style="box-sizing: border-box;">Manufacturer Name: Miabella</li></ul></div><div style="'
                                               'font-size: medium;"><ul class="list-unstyled" style="box-sizing: border-box; '
                                               'margin-top: 0px; margin-bottom: 10px; padding-left: 0px; list-style: none; color: '
                                               'rgb(51, 51, 51); font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif;">'
                                               '<li style="box-sizing: border-box;"></li></ul></div></div></h3></div><div><div style="">'
                                               '<ul class="list-unstyled" style="box-sizing: border-box; margin-top: 0px; margin-bottom: '
                                               '10px; padding-left: 0px; list-style: none; color: rgb(51, 51, 51); font-family: '
                                               '&quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; background-color: '
                                               'rgb(255, 255, 255);"><li style="box-sizing: border-box;"><h3 style="color: inherit; '
                                               'font-family: inherit; box-sizing: border-box; font-weight: 500; line-height: 1.1; margin-top: '
                                               '20px; margin-bottom: 10px; font-size: 24px;"><p style="font-size: medium; box-sizing: '
                                               'border-box; margin: 0px 0px 10px;">' + description+ '</p></h3><h3 style="color: '
                                               'inherit; font-family: inherit; box-sizing: border-box; font-weight: 500; line-height: 1.1; '
                                               'margin-top: 20px; margin-bottom: 10px; font-size: 24px;"><div style="font-family: '
                                               'Arial; font-size: 14pt;"><ul style="box-sizing: border-box; margin-top: 0px; '
                                               'margin-bottom: 10px; font-family: &quot;Helvetica Neue&quot;, Helvetica, Arial, '
                                               'sans-serif; font-size: medium;"></ul></div></h3><hr><h3 style="box-sizing: border-box; '
                                               'font-family: inherit; font-weight: 500; line-height: 1.1; color: inherit; margin-top: 20px; '
                                               'margin-bottom: 10px; font-size: 24px;">Handling</h3><p style="font-size: medium; box-sizing: '
                                               'border-box; margin: 0px 0px 10px; margin-bottom: 20px;">We will ship all orders within&nbsp;'
                                               '<mark style="box-sizing: border-box; background: rgb(252, 248, 227); padding: 0.2em;">'
                                               '3 business days</mark>&nbsp;of payment. We take great care packaging every item to '
                                               'ensure safe and quality shipping</p></li><li style="box-sizing: border-box;"><hr>'
                                               '<h3 style="box-sizing: border-box; font-family: inherit; font-weight: 500; line-height: 1.1; '
                                               'color: inherit; margin-top: 20px; margin-bottom: 10px; font-size: 24px;"><span class="'
                                               'glyphicon glyphicon-send" style="box-sizing: border-box; position: relative; top: 1px; '
                                               'display: inline-block; font-family: &quot;Glyphicons Halflings&quot;; line-height: 1; '
                                               '-webkit-font-smoothing: antialiased;"></span>Delivery</h3></li><p style="font-size: '
                                               'medium; box-sizing: border-box; margin: 0px 0px 10px; margin-bottom: 20px;">We will '
                                               'ship UPS/USPS/FedEx depending on your location and our discretion. Please make sure '
                                               'to provide the correct shipping address when placing your order. Packages are NOT '
                                               'sent out on Saturday or Sunday and transit times may vary depending on the carrier. '
                                               'Shipping time by eBay are not guaranateed and are subject to change especially during '
                                               'peak periods.</p><li style="box-sizing: border-box;"><hr><h3 style="box-sizing: border-box; '
                                               'font-family: inherit; font-weight: 500; line-height: 1.1; color: inherit; margin-top: 20px; '
                                               'margin-bottom: 10px; font-size: 24px;">Feedback<span class="glyphicon glyphicon-ok-circle" '
                                               'style="box-sizing: border-box; position: relative; top: 1px; display: inline-block; '
                                               'font-family: &quot;Glyphicons Halflings&quot;; line-height: 1; -webkit-font-smoothing: '
                                               'antialiased;"></span></h3></li><li style="box-sizing: border-box;"><p style="font-size: '
                                               'medium; box-sizing: border-box; margin: 0px 0px 10px; margin-bottom: 20px;">We take '
                                               'our reputation seriously, we buy and sell online, so we understand the value of trust.'
                                               '&nbsp;<mark style="box-sizing: border-box; background: rgb(252, 248, 227); padding: '
                                               '0.2em;">If you are unsatisfied with your order, please contact us</mark>&nbsp;and we '
                                               'will work with you to resolve it to your satisfaction. Please allow 1-3 days for a '
                                               'response to all inquiries.</p></li></ul><div></div></div></div></font>]]>',

                                "PrimaryCategory": {"CategoryID": category},
                                "StartPrice": sale_price,
                                "PictureDetails": {"PictureURL": image_list},

                                "Country": "US",
                                "Currency": "USD",
                                "ConditionID": "1000",
                                "CategoryMappingAllowed": "true",
                                "DispatchTimeMax": "3",
                                "ListingDuration": "Days_30",
                                "Quantity": "1",

                                "PaymentMethods": "PayPal",
                                "PayPalEmailAddress": "ngs5st@virginia.edu",
                                "PostalCode": "23505",

                                "ReturnPolicy": {
                                    "ReturnsAcceptedOption": "ReturnsNotAccepted",
                                },

                                "ProductListingDetails": {
                                    "UPC": str(int(upc_value)),
                                    "Brand": "MiaBella"
                                },

                                "ShippingDetails": {
                                    "ShippingType": "Flat",
                                    "ShippingServiceOptions": {
                                        "ShippingServicePriority": "1",
                                        "ShippingService": "UPS2ndDay",
                                        "ShippingServiceCost": "0"
                                    }
                                },

                                "Site": "US"

                            }
                        }

                        #r = api.execute("AddFixedPriceItem", myitem)

                    else:
                        pass

                except ConnectionError as e:

                    if counter < 5:

                        print('')
                        print("Currently Waiting Before Retrying Listing - ConnectionError: {}/5".format(counter))
                        print("Error: ", e)
                        print('')

                        time.sleep(60)
                        counter += 1
                        continue

                    else:

                        print('')
                        print("Currently Waiting Before Retrying Listing - ConnectionError: {}/5".format(counter))
                        print("Error: ", e)
                        print('')

                        time.sleep(60)

                counter = 0
                break

    else:
        print("Invalid Category")