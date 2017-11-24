#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
import ScrapyCrawler


process = CrawlerProcess({
   # 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.type=0; Winfile=dows NT 5.1)'
})

process.crawl(ScrapyCrawler.PropertiesSpider)
process.start()