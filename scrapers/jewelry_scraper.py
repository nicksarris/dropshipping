__author__ = 'Nick Sarris (ngs5st)'

import re
import time
import numpy as np
import pandas as pd
from wapy.wapy.api import Wapy
from ebaysdk.finding import Connection as finding
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError

def data_cleanup():

    merchandise = pd.read_csv('data/jewelry_crosschecked.csv', encoding='ISO-8859-1')

    merchandise['sale_price'] = merchandise['sale_price'].map(lambda x: float(x))
    merchandise['name'] = merchandise['name'].map(lambda x: x.strip())
    merchandise['name'] = merchandise['name'].map(lambda x: str(x).replace('"',''))

    merchandise = merchandise[merchandise['sale_price'] > 50]
    merchandise = merchandise[merchandise['sale_price'] < 300]
    merchandise = merchandise[merchandise['stock'] == 'Available']
    merchandise = merchandise[np.isfinite(merchandise['upc'])]
    merchandise = merchandise.drop_duplicates()

    merchandise.to_csv('data/finalized_data.csv', index=False)

def walmart_jewelry(walmart_key):

    final_list = []
    item_list = []

    wapy = Wapy(walmart_key)
    for i in range(1, 40):
        print('Scraping from Page: {}'.format(i))
        items = wapy.search('Miabella', categoryId=3891, numItems=25, page=i)
        for item in items:
            list.append(item_list, item)

    headers = ['item_id','name','sale_price','short_description',
               'long_description','images','stock','upc']

    for item in item_list:
        data = [item.item_id, item.name, item.sale_price,
                item.short_description, item.long_description,
                item.images, item.stock, item.upc]

        list.append(final_list, data)

    output_df = pd.DataFrame(final_list, columns=headers)
    output_df.to_csv('data/jewelry_merchandise.csv', index=False)

def ebay_jewelry():

    final_list = []
    merchandise = pd.read_csv('data/jewelry_merchandise.csv', encoding='ISO-8859-1')
    api = finding(config_file='data/ebay_auth.yaml')

    headers = ['item_id','name','sale_price','short_description',
               'long_description','images','stock','upc']

    for i, item in merchandise.iterrows():

        try:

            response = api.execute(
                'findItemsAdvanced', {
                'keywords': item['name'],
                'paginationInput': {
                    'entriesPerPage': '25',
                    'pageNumber': '1'
                },
                'sortOrder': 'BestMatch'
            })

            item_values = []
            dictstr = response.reply.get('searchResult')
            if dictstr.get('_count') != '0':
                clearedArray = dictstr.get('item')
                for listing in clearedArray:
                    list.append(item_values,
                        listing.get('sellingStatus')
                               .get('currentPrice')
                               .get('value'))

            value_flag = True
            for value in item_values:
                if float(value) < float(item['sale_price']):
                    value_flag = False

            if value_flag == True:
                print(i, item['name'])
                list.append(final_list,
                    [item['item_id'],
                     item['name'],
                     item['sale_price'],
                     item['short_description'],
                     item['long_description'],
                     item['images'],
                     item['stock'],
                     item['upc']])

        except ConnectionError as e:
            pass

    output_df = pd.DataFrame(final_list, columns=headers)
    output_df.to_csv('data/jewelry_crosschecked.csv', index=False)