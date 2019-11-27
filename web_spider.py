
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.signalmanager import dispatcher
from pprint import pprint


class WebSpider(scrapy.Spider):

    name = 'webspider'

    def parse(self, response):
        for post in response.css('div.blog-item'):
            yield {
                'date': post.css('div.blog-date h5::text').get(),
                'title': post.css('div.blog-title h3::text').get()
            }


def run_spider(spider_class, allowed_domain, start_urls):

    result = []

    def crawler_results(signal, sender, item, response, spider):
        result.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(settings={'LOG_ENABLED': True})
    process.crawl(spider_class, allowed_domain=allowed_domain, start_urls=start_urls)
    process.start()  # the script will block here until the crawling is finished

    return result


if __name__ == '__main__':
    data = run_spider(WebSpider, ['hiwijaya.com'], ['https://hiwijaya.com'])
    pprint(data)
