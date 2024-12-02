import scrapy
from scrapy_playwright.page import PageMethod


class Website3MultiplePagesSpider(scrapy.Spider):
    name = "website3multiplepagesspider"
    allowed_domains = ["sundayobserver.lk"]
    start_urls = ["https://www.sundayobserver.lk/category/obituaries/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_coroutines": [
                        PageMethod("wait_for_selector", "li.list-post.pclist-layout"),
                    ],
                },
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        try:
            while True:
                # Extract links from the current page
                obituary_links = response.xpath("//h2[contains(@class, 'penci-entry-title')]/a/@href").getall()
                for link in obituary_links:
                    yield scrapy.Request(
                        url=response.urljoin(link),
                        callback=self.parse_obituary,
                        meta={
                            "playwright": True,
                            "playwright_page_coroutines": [
                                PageMethod("wait_for_selector", "div.entry-content"),
                            ],
                        },
                    )

                # Attempt to click the "Load More" button
                load_more_button = await page.query_selector("a.penci-ajax-more-button")
                if load_more_button:
                    self.logger.info("Clicking 'Load More' button.")
                    await load_more_button.click()
                    await page.wait_for_timeout(2000)  # Wait for content to load
                else:
                    self.logger.info("No 'Load More' button found. End of records.")
                    break

                # Refresh response content
                new_content = await page.content()
                response = scrapy.http.HtmlResponse(
                    url=response.url,
                    body=new_content,
                    encoding="utf-8",
                )
        except Exception as e:
            self.logger.error(f"Error while processing: {e}")
        finally:
            await page.close()

    async def parse_obituary(self, response):
        try:
            # Extract obituary content
            content_paragraphs = response.xpath("//div[contains(@class, 'entry-content')]/p/text()").getall()
            obituary_note = " ".join([text.strip() for text in content_paragraphs if text.strip()])

            # Extract meta-information
            date_time = response.xpath("//div[contains(@class, 'post-box-meta-single')]/span[1]/text()").get(default="N/A").strip()
            comments = response.xpath("//div[contains(@class, 'post-box-meta-single')]/span[2]/text()").get(default="N/A").strip()
            views = response.xpath("//div[contains(@class, 'post-box-meta-single')]/span[3]/i[@class='penci-post-countview-number']/text()").get(default="N/A").strip()

            yield {
                "Obituary URL": response.url,
                "Obituary Note": obituary_note,
                "Date and Time": date_time,
                "Comments": comments,
                "Views": views,
            }
        except Exception as e:
            self.logger.error(f"Error while parsing obituary: {e}")
