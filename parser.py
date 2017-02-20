# file to parse magicmonk for cards
# -*- coding: utf-8 -*-
from lxml import html
import requests

search_url = """ http://magicmonk.ch/epages/170349.sf/de_CH/?ObjectID=17173
&ViewAction=FacetedSearchProducts&SearchString= """
host = 'http://magicmonk.ch'

def getTree(searchString):
    url = search_url + searchString
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree


searchString = ''
tree = getTree(searchString)
itemSelector = '//div[contains(@class,"ListItemProductContainer")]'
itemInfoSelector = '//div[contains(@class,"ListItemProductInfoContainer")]'
itemNameSelector = itemSelector+'//h3[@class="Headline"]/a/span[@itemprop="name"]/text()'
itemImageSelector = itemSelector+'//img[@class="ProductSmallImage"]//@src'
itemStockCountSelector = itemSelector+itemInfoSelector+'//i[@class="Icon ProductOnStockIcon"]/following-sibling::text()[1]'
itemPriceSelector = itemSelector+itemInfoSelector+'//div[@class="PriceArea"]//span[@class="price-value"]/text()'

itemNames = tree.xpath(itemNameSelector)
itemImages = tree.xpath(itemImageSelector)
itemStockCount = tree.xpath(itemStockCountSelector)
itemPrices = tree.xpath(itemPriceSelector)


# post processing for correct information
for item in itemNames:
    print item.encode(encoding='UTF-8', errors='ignore')
for image in itemImages:
    image = host+image.replace('_s.', '_ml.')
    # print image
for stockCount in itemStockCount:
    stockCount = '#'+stockCount.split()[0]
    print stockCount
for price in itemPrices:
    print 'CHF: ' + price.split()[1]

if __name__ == '__main__':
    closeInput = raw_input("Press ENTER to exit")
