import scrapy


class Website1spiderSpider(scrapy.Spider):
    name = "website1spider"
    allowed_domains = ["www.elanka.com.au"]
    start_urls = ["https://www.elanka.com.au/obituaries/"]

    def parse(self, response):
        obituaries = response.css('.pld-post-list-inr')

        for obituary in obituaries:
            yield{
                'Obituary': obituary.css('h2 a::text').get(),
                'Date': obituary.css('.pld-post-meta span::text').get(),
            }
        
        next_page_url = response.css('div.pld-pagination a.page-numbers.next::attr(href)').get()
        
        if next_page_url:
            # Follow the next page only if the URL exists
            yield response.follow(next_page_url, callback=self.parse)