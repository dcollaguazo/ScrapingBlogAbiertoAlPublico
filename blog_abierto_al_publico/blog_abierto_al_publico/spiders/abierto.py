import scrapy
import codecs
from scrapy import Request

class QuotesSpider(scrapy.Spider):
    name = "abierto"
    allowed_domains = ["blogs.iadb.org"]
    start_urls = [
    'https://blogs.iadb.org/abierto-al-publico/2014/',
    'https://blogs.iadb.org/abierto-al-publico/2015/',
    'https://blogs.iadb.org/abierto-al-publico/2016/',
    'https://blogs.iadb.org/abierto-al-publico/2017/',
    'https://blogs.iadb.org/abierto-al-publico/2018/',
    ]

    def parse(self, response):
        articles = response.xpath('//div[@class="blog-item-inner"]')

        for article in articles:
            author = article.xpath('div[@class="blog-info-wrapper"]/div[@class="blog-author"]/a/text()').extract_first()
            publication_date = article.xpath('div[@class="blog-info-wrapper"]/div[@class="blog-date"]/a/text()').extract_first()
            title = article.xpath('div[@class="blog-context"]/h2[@class="blog-title"]/a/text()').extract_first()
            blog_url = article.xpath('div[@class="blog-context"]/h2[@class="blog-title"]/a/@href').extract_first()
            summary = article.xpath('div[@class="blog-context"]/div[@class="blog-excerpt"]/text()').extract_first()


            request = scrapy.Request(url=blog_url, callback=self.parse_blog)
            request.meta['author'] = author.strip()
            request.meta['publication_date'] = publication_date
            request.meta['title'] = title
            request.meta['summary'] = summary
            request.meta['blog_url'] = blog_url

            yield request

        # follow pagination link
        current_url = article.xpath('//link[@rel="canonical"]/@href').extract_first()
        next_url = article.xpath('//link[@rel="next"]/@href').extract_first()
        if next_url!=None:
            yield scrapy.Request(url=next_url, callback=self.parse)
        

    def parse_blog(self, response):
        author = response.meta['author']
        publication_date = response.meta['publication_date']
        title = response.meta['title']
        summary = response.meta['summary']
        blog_url = response.meta['blog_url']
        blog_content = response.xpath('normalize-space(//div[@class = "pf-content"])').extract()

        
        yield{
                'author': author,
                'publication_date': publication_date,
                'title': title,
                'summary': summary,
                'blog_url': blog_url,
                'blog_content': blog_content,

            }
        

