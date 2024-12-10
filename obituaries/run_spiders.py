from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from obituaries.spiders.website1 import Website1Spider
from obituaries.spiders.website2 import Website2Spider
from obituaries.spiders.website3 import Website3Spider
from obituaries.spiders.website4 import Website4Spider

def run_spiders():
    process = CrawlerProcess(get_project_settings())

    # Add all spiders to the process
    process.crawl(Website1Spider)
    process.crawl(Website2Spider)
    process.crawl(Website3Spider)
    process.crawl(Website4Spider)

    # Start crawling
    process.start()

if __name__ == "__main__":
    run_spiders()
