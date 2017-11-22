from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class PropertiesSpider(CrawlSpider):
    name = "electronics"
    allowed_domains = ["www.propertymarket.com.mt"]

    #pc7 Bungalow
    start_urls = [
        'http://www.propertymarket.com.mt/for-sale/?pt=0&currentLocations=&mnp=0&mxp=0&pc=7&nb=0&btnForSale=Search'
    ]
    rules = (
        # Rule(LinkExtractor(restrict_xpaths='.//a[@title="Next"]'),
        #      callback="parse_page",
        #      follow=True),

        Rule(LinkExtractor(
            allow=(r'/view'),
            restrict_xpaths='.//div[@class="searchResultListingPrice "]/a[@id="searchResultListingLink"]'),
            callback="parse_item",
            follow=False),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.property_type = "bungalow"
        self.file_name = "Data/malta_properties.json"

    def parse_page(self, response):
        print('Page Processing..' + response.url)

    def parse_item(self, response):
        hxs = Selector(response)

        property_type = self.property_type
        title = hxs.xpath('//div[@id="myListingDetailsTitle"]/h1[@class="entry-title"]/text()')[0].extract()
        price = hxs.xpath('//div[@id="myListingDetailsPrice"]/text()')[0].extract()

        description = "";
        descriptions = hxs.xpath('//div[@class="listingDetailsDescription"]/text()').extract()
        for d in descriptions:
            d.replace('\r', '').replace('\t', '').replace('\n', '').strip()
            if d:
                description += (d + " ")

        description = description.strip()

        details = hxs.xpath('//div[@class="listingDetailsDescriptionFooter"]/span/node()').extract()
        features = hxs.xpath('//div[@class="listingDetailsFeatures"]/div/text()').extract()


        print('{0} {1} {2} {3}'.format(property_type, title, price, description))
        print(details)
        print(features)