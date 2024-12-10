# Scrapy settings for obituaries project
BOT_NAME = "obituaries"

SPIDER_MODULES = ["obituaries.spiders"]
NEWSPIDER_MODULE = "obituaries.spiders"

ITEM_PIPELINES = {
    'obituaries.pipelines.ObituariesPipeline': 300,
}

# Configure the Scrapy Playwright handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Use Chromium for Playwright
PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Use the asyncio-based reactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Concurrent requests per domain
CONCURRENT_REQUESTS = 8

# Enable Playwright retries for better JS website scraping
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # 1 minute

# Increase download delay to avoid blocking
DOWNLOAD_DELAY = 1  # 1-second delay between requests

# Lower concurrent Playwright pages to avoid resource contention
CONCURRENT_REQUESTS_PER_DOMAIN = 4
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 2

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
