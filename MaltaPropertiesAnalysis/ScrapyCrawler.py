#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import re


class PropertiesSpider(CrawlSpider):
    name = "property_marker"
    allowed_domains = ["www.propertymarket.com.mt"]

    #pc 7 Bungalow
    #pc 101 Penthouse
    #pc 1 Houses and Villas
    start_urls = [
        'http://www.propertymarket.com.mt/for-sale/?pt=0&currentLocations=&mnp=0&mxp=0&pc=1&nb=0&btnForSale=Search'
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths='.//a[@title="Next"]'),
             callback="parse_page",
             follow=True),

        Rule(LinkExtractor(
            allow=(r'/view'),
            restrict_xpaths='.//div[@class="searchResultListingPrice "]/a[@id="searchResultListingLink"]'),
            callback="parse_item",
            follow=False),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.property_type = "villa"
        self.file_name = "data/malta_{0}_properties.json".format(self.property_type)
        self.file = open(self.file_name, 'w', encoding='utf8');

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.file.close();

    def parse_page(self, response):
        print('Page Processing..' + response.url)

    def parse_item(self, response):
        hxs = Selector(response)

        property_type = self.property_type
        title = hxs.xpath('//div[@id="myListingDetailsTitle"]/h1[@class="entry-title"]/text()')[0].extract()
        price = hxs.xpath('//div[@id="myListingDetailsPrice"]/text()')[0].extract()
        price = price.replace('\r', '').replace('\t', '').replace('\n', '').strip()

        description = "";
        descriptions = hxs.xpath('//div[@class="listingDetailsDescription"]/text()').extract()
        for d in descriptions:
            d.replace('\r', '').replace('\t', '').replace('\n', '').strip()
            if d:
                description += (d + " ")

        description = description.strip()

        details = hxs.xpath('//div[@class="listingDetailsDescriptionFooter"]/span').extract()
        details_dict = {}

        for d in details:
            name_groups = re.search('.*<strong> *(.+?) *: *</strong>.*', d)
            if name_groups:
                name = name_groups.group(1)
                value_group = re.search('.*</strong> *(.+?) *</span>.*', d)
                if value_group:
                    value = value_group.group(1)
                    details_dict[name] = value

        features = hxs.xpath('//div[@class="listingDetailsFeatures"]/div/text()').extract()
        features_improved = []
        for f in features:
            feature = f.replace('\r', '').replace('\t', '').replace('\n', '').strip()
            features_improved.append(feature)

        print('{0} {1} {2} {3}'.format(property_type, title, price, description))
        print(details_dict)
        print(features_improved)

        id = details_dict['Ref']
        details_dict.pop('Ref', None)

        item = {'id': id, 'type': property_type, 'title': title, 'price': price, 'description': description,
                              'details': details_dict, 'features': features_improved}

        json_str = json.dumps(item).encode('utf8').decode('utf8')
        self.file.write(json_str)
        self.file.write('\n')
