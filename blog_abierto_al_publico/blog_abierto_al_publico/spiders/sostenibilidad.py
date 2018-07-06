import scrapy
import codecs
from scrapy import Request
counter = 1

class QuotesSpider(scrapy.Spider):
    name = "sostenibilidad"
    allowed_domains = ["blogs.iadb.org"]
    start_urls = ['https://blogs.iadb.org/sostenibilidad/2011/',
    'https://blogs.iadb.org/sostenibilidad/2012/',
    'https://blogs.iadb.org/sostenibilidad/2013/',
    'https://blogs.iadb.org/sostenibilidad/2014/',
    'https://blogs.iadb.org/sostenibilidad/2015/',
    'https://blogs.iadb.org/sostenibilidad/2016/',
    'https://blogs.iadb.org/sostenibilidad/2017/',
    'https://blogs.iadb.org/sostenibilidad/2018/',
    ]
       

    def parse(self, response):
        global counter
        articles = response.xpath('//article[@class="item-medium post-box-big"]')

        for article in articles:
            author = article.xpath('div[@class="meta-info"]/span[@class="entry-author"]/a/text()').extract_first()
            publication_date = article.xpath('div[@class="meta-info"]/time[@class="entry-date"]/@datetime').extract_first()
            title = article.xpath('h3[@class="entry-title"]/a/@title').extract_first()
            summary = article.xpath('div[@class="i-summary"]/p/text()').extract_first()
            views = article.xpath('div[@class="meta-count no-bottom"]/div[@class="count-data"]/span[@class="meta-info-viewer"]/text()').extract_first()
            number_comments = article.xpath('div[@class="meta-count no-bottom"]/div[@class="count-data"]/span[@class="meta-info-comments"]/a/text()').extract_first()
            blog_url = article.xpath('h3[@class="entry-title"]/a/@href').extract_first()
            
            request = scrapy.Request(url=blog_url, callback=self.parse_blog)
            request.meta['author'] = author.strip()
            request.meta['publication_date'] = publication_date
            request.meta['title'] = title
            request.meta['summary'] = summary
            request.meta['views'] = views
            request.meta['number_comments'] = number_comments
            request.meta['blog_url'] = blog_url

            yield request

        # follow pagination link
        next_page_urls = response.xpath('//div[@class="pagination"]/a/@href').extract()
        

        if len(next_page_urls)>0:
            for page in next_page_urls:
                if counter <= len(next_page_urls):
                    yield scrapy.Request(url=page, callback=self.parse)
                    counter+=1



    def parse_blog(self, response):

        author = response.meta['author']
        publication_date = response.meta['publication_date']
        title = response.meta['title']
        summary = response.meta['summary']
        views = response.meta['views']
        number_comments = response.meta['number_comments']
        blog_url = response.meta['blog_url']
        blog_content = response.xpath('normalize-space(//div[@class = "text-content"])').extract()

        yield{
                'author': author,
                'publication_date': publication_date,
                'title': title,
                'summary': summary,
                'views': views,
                'number_comments': number_comments,
                'blog_url': blog_url,
                'blog_content': blog_content,

            }

