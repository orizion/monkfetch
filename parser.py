# file to parse magicmonk for cards
#
from lxml import html
from lxml import etree
import requests
import unicodedata

search_url = """ http://magicmonk.ch/epages/170349.sf/de_CH/?ObjectID=17173
&ViewAction=FacetedSearchProducts&SearchString= """
host = 'http://magicmonk.ch'

def normalize(data):
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    return normal

def getTree(searchString):
    url = search_url + searchString
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree


def getItemData():
    searchString = ''
    tree = getTree(searchString)
    stringify = etree.XPath("string()")
    itemSelector = '//div[contains(@class,"ListItemProductContainer")]'
    itemInfoSelector = '//div[contains(@class,"ListItemProductInfoContainer")]'
    itemNameSelector = itemSelector+'//h3[@class="Headline"]/a/span[@itemprop="name"]/text()'
    itemImageSelector = itemSelector+'//img[@class="ProductSmallImage"]//@src'
    itemStockCountSelector = itemSelector+itemInfoSelector+'//i[@class="Icon ProductOnStockIcon"]/following-sibling::text()[1]'
    itemPriceSelector = itemSelector+itemInfoSelector+'//div[@class="PriceArea"]//span[@class="price-value"]/text()'

    itemNames = tree.xpath(itemNameSelector)
    itemImages = tree.xpath(itemImageSelector)
    itemStockCounts = tree.xpath(itemStockCountSelector)
    itemPrices = tree.xpath(itemPriceSelector)


    # post processing for correct information
    for i in xrange(len(itemNames)):
         itemNames[i] = itemNames[i]
    for i in xrange(len(itemImages)):
        itemImages[i] = host+itemImages[i].replace('_s.', '_ml.')
    # print image
    for i in xrange(len(itemStockCounts)):
        itemStockCounts[i] = itemStockCounts[i].split()[0]
    for i in xrange(len(itemPrices)):
        itemPrices[i] =  'CHF: ' + itemPrices[i].split()[1]

    items = zip(itemNames,itemPrices,itemStockCounts,itemImages)
    for item in items:
        print item

if __name__ == '__main__':
    getItemData()
    closeInput = raw_input("Press ENTER to exit")
