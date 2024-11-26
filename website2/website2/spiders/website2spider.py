import scrapy


class Website2spiderSpider(scrapy.Spider):
    name = "website2spider"
    allowed_domains = ["reserved767.rssing.com"]
    start_urls = ["https://reserved767.rssing.com/chan-65241722/all_p1.html"]

    def parse(self, response):
        obituaries = response.css('header.cs-post-single-title')
        posts = response.css('div.cs-single-post-content')
        for obituary in obituaries:
            yield {
                'Obituary': obituary.css('h1 a::text').get(),
                'Date': obituary.css('div span::text').get(),               
            }
           
        # Extract the next page URL
        next_page = response.css('a.cs-btn.cs-btn-small[title="newer"]::attr(href)').get()


        if next_page:
            # Build the full URL and follow it
            next_page_url = 'https:'+ next_page
            yield response.follow(next_page_url, callback=self.parse)