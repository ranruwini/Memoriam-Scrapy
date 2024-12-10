import scrapy
from scrapy_playwright.page import PageMethod

class Website4Spider(scrapy.Spider):
    name = "website4spider"

    def start_requests(self):
            yield scrapy.Request(
                url='https://www.dailynews.lk/2024/10/21/obituaries/657697/obituaries-332/',
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', '.pcrlt-style-1')
                    ],
                )
            )

    async def parse(self, response):
        # Get the Playwright page object
        page = response.meta["playwright_page"]

        
        try:
            # Extract and yield obituaries on the current page
            obituaries = response.css('div.item-related-inner')
            for obituary in obituaries:
                note = obituary.css('div.related-content h3 a::text').get()
                date = obituary.css('div.related-content span time::text').get()
                
                yield{
                    "Obituary Note": note,
                    "Date": date,
                    }
        
        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            

        await page.close()