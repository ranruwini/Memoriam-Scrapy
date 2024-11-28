import scrapy
from scrapy_playwright.page import PageMethod


class Website3Spider(scrapy.Spider):
    name = "website3spider"

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.sundayobserver.lk/category/obituaries/',
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'li.list-post.pclist-layout')
                ],
            )
        )

    async def parse(self, response):
        # Get the Playwright page object
        page = response.meta["playwright_page"]

        # Keep clicking "Load More" until no more button is available
        while True:
            try:
                # Extract and yield obituaries on the current page
                obituaries = response.css('li.list-post.pclist-layout')
                for ob in obituaries:
                    date = ob.css('time.entry-date.published::text').get(default="Date not found")
                    note = ob.css('div.item-content.entry-content p::text').get(default="Note not found")
                    yield {
                        "Published Date": date,
                        "Obituary Note": note,
                    }

                load_more_button = await page.query_selector('a.penci-ajax-more-button')
                if load_more_button:
                    await load_more_button.click()
                    await page.wait_for_timeout(2000)
                else:
                    break  

                content = await page.content()
                response = scrapy.http.TextResponse(
                    url=page.url,
                    body=content,
                    encoding='utf-8',
                )
            except Exception as e:
                self.logger.error(f"Error occurred: {e}")
                break

        # Close the Playwright page after all data is scraped
        await page.close()
