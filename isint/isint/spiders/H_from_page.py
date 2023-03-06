import scrapy
from isint.items import ItemHsFromPage


def get_urls_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()
        return data.split()


class HsFromPage(scrapy.Spider):
    name = 'hs_from_page'
    start_urls = get_urls_from_file('urls.txt')

    def parse(self, response, **kwargs):
        h1 = response.xpath('//h1/text()').getall()
        h2 = response.xpath('//h2/text()').getall()

        h3 = response.xpath('//h3/text()').getall()
        h4 = response.xpath('//h4/text()').getall()
        item = ItemHsFromPage(
            site=response.url,
            response_kod=response.status,
            h1=h1,
            h2=h2,
            h3=h3,
            h4=h4
        )
        yield item
        # self.log(response.url)
        # print()
