import scrapy

class EgrulItsoft(scrapy.Spider):
    name = 'egrul_itsoft'
    start_urls = ['https://egrul.itsoft.ru/',]
    inn = None
    start = True

    def parse(self, response, **kwargs):
        if self.start:
            self.start = False
            next_page = self.generate_url()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
        else:
            yield {'data': response.xpath('СвЮЛ/СвНаимЮЛ/СвНаимЮЛСокр/@НаимСокр').get()}
            next_page = self.generate_url()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def generate_url(self):
        self.get_inn()
        return f'https://egrul.itsoft.ru/{self.inn}.xml'

    def get_inn(self):
        self.inn = '9704189831'

