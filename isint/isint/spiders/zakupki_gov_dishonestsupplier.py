import scrapy
from datetime import datetime, timedelta, date
from isint.items import ItemZakupkiDishonest
from scrapy.loader import ItemLoader


class ZakupkiDishonest(scrapy.Spider):
    name = 'zakupki_dishonest'
    # allowed_domains = ['https://zakupki.gov.ru/']
    start_date = datetime.strptime('01.01.2021', "%d.%m.%Y").date()
    finish_date = datetime.strptime('14.01.2021', "%d.%m.%Y").date()
    page_number = 1
    start_urls = [f'https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?morphology=on&search-filter=Дате+размещения&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on&inclusionDateFrom={start_date.strftime("%d.%m.%Y")}&inclusionDateTo={finish_date.strftime("%d.%m.%Y")}',]
###
    def parse(self, response, **kwargs):
        result = []
        cards = response.xpath('//div[@class="row no-gutters registry-entry__form mr-0"]')
        for card in cards:
            add, delete, update = '', '', ''
            fz = card.xpath('.//div[@class="registry-entry__header-top__title text-truncate"]/text()').get().strip()

            number = card.xpath('.//div[@class="registry-entry__header-mid__number"]/a/text()').get().strip()
            href = card.xpath('.//div[@class="registry-entry__header-mid__number"]/a/@href').get()
            name = card.xpath('.//div[@class="registry-entry__body-value"]/text()').getall()[0]
            inn = card.xpath('.//div[@class="registry-entry__body-value"]/text()').getall()[1]
            status = card.xpath('.//div[contains(@class,"registry-entry__header-mid__title")]/text()').get().strip()
            time_s = card.xpath('.//div[@class="col d-flex flex-column registry-entry__right-block b-left "]')
            time_ = time_s.xpath('.//div[@class="data-block__value"]/text()').getall()
            if len(time_) == 2:
                add = time_[0].strip()
                delete = ''
                update = time_[1].strip()
            elif len(time_) == 3:
                add = time_[0].strip()
                delete = time_[2].strip()
                update = time_[1].strip()
            else:
                add = time_[0].strip()
                delete = ''
                update = ''
            item = ItemZakupkiDishonest(
                fz=fz,
                number=number,
                href=href,
                name=name,
                inn=inn,
                status=status,
                add=add,
                delete=delete,
                update=update
            )
            yield item
        # yield {'url': response.url}
        next_page = response.xpath('//a[@class="paginator-button paginator-button-next"]/@data-pagenumber').get()
        if next_page is not None:
            next_url = response.url.replace(f'pageNumber={str(self.page_number)}',
                                            f'pageNumber={str(self.page_number + 1)}')
            self.page_number += 1
            yield response.follow(next_url, callback=self.parse)
        else:
            self.page_number = 1
   #https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?searchString=&morphology=on&search-filter=Дате+обновления&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&pageNumber=19&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on&dsStatuses=&inclusionDateFrom=01.02.2022&inclusionDateTo=28.02.2022&lastUpdateDateFrom=&lastUpdateDateTo=
            next_page_change_date = self.generate_url()
            if next_page_change_date is not None:
                yield response.follow(next_page_change_date, callback=self.parse)

    def generate_url(self):
        self.start_date = self.finish_date + timedelta(days=1)
        self.finish_date += timedelta(days=15)
        if self.finish_date > datetime.strptime('31.12.2022', "%d.%m.%Y").date():
            self.finish_date = datetime.strptime('31.12.2022', "%d.%m.%Y").date()
        if self.start_date >= datetime.strptime('31.12.2022', "%d.%m.%Y").date():
            return None
        return f'https://zakupki.gov.ru/epz/dishonestsupplier/search/results.html?morphology=on&search-filter=Дате+размещения&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&fz94=on&fz223=on&ppRf615=on&inclusionDateFrom={self.start_date.strftime("%d.%m.%Y")}&inclusionDateTo={self.finish_date.strftime("%d.%m.%Y")}'




