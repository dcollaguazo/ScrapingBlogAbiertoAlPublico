import scrapy
# import logging
from scrapy import Request

class QuotesSpider(scrapy.Spider):
    name = "blogs_iadb"
    allowed_domains = ["blogs.iadb.org"]
    start_urls = [
    'https://blogs.iadb.org/conocimiento-abierto/es/',
    'https://blogs.iadb.org/conocimiento-abierto/en/',
    'https://blogs.iadb.org/transporte/es/',
    'https://blogs.iadb.org/transporte/en/',
    'https://blogs.iadb.org/agua/es/',
    'https://blogs.iadb.org/agua/en/',
    'https://blogs.iadb.org/gestion-fiscal/es/',
    'https://blogs.iadb.org/gestion-fiscal/en/',
    'https://blogs.iadb.org/ideas-que-cuentan/es/',
    'https://blogs.iadb.org/integracion-comercio/es/',
    'https://blogs.iadb.org/integration-trade/en/',
    'https://blogs.iadb.org/salud/es/',
    'https://blogs.iadb.org/salud/en/',
    'https://blogs.iadb.org/energia/es/',
    'https://blogs.iadb.org/energia/en/',
    'https://blogs.iadb.org/ciudades-sostenibles/es/',
    'https://blogs.iadb.org/ciudades-sostenibles/en/',
    'https://blogs.iadb.org/desarrollo-infantil/es/',
    'https://blogs.iadb.org/desarrollo-infantil/en/',
    'https://blogs.iadb.org/industrias-creativas/es/',
    'https://blogs.iadb.org/industrias-creativas/en/',
    'https://blogs.iadb.org/administracion-publica/es/',
    'https://blogs.iadb.org/administracion-publica/en/',
    'https://blogs.iadb.org/educacion/es/',
    'https://blogs.iadb.org/educacion/en/',
    'https://blogs.iadb.org/efectividad-desarrollo/es/',
    'https://blogs.iadb.org/efectividad-desarrollo/en/',
    'https://blogs.iadb.org/trabajo/es/',
    'https://blogs.iadb.org/sostenibilidad/es/',
    'https://blogs.iadb.org/sostenibilidad/en/',
    'https://blogs.iadb.org/seguridad-ciudadana/es/',
    'https://blogs.iadb.org/seguridad-ciudadana/en/',
    'https://blogs.iadb.org/innovacion/es/',
    'https://blogs.iadb.org/igualdad/es/',
    'https://blogs.iadb.org/igualdad/en/',
    'https://blogs.iadb.org/bidinvest/es/',
    'https://blogs.iadb.org/bidinvest/en/',
    ]

    def parse(self, response):
        # self.logger.info('Parse function called on %s', response.url)
        articles = response.xpath('//article')

        for article in articles:
            author = article.xpath('header[@class="entry-header"]/p[@class="entry-meta"]/a/text()').extract_first(default='')
            publication_date = article.xpath('header[@class="entry-header"]/p[@class="entry-meta"]/time[@class="entry-time"]/text()').extract_first(default='')
            title = article.xpath('header[@class="entry-header"]/h2[@class="entry-title"]/a/text()').extract_first(default='')
            blog_url = article.xpath('header[@class="entry-header"]/h2/a/@href').extract_first(default='')
            summary = article.xpath('div[@class="entry-content"]/p/text()').extract_first(default='')
            
            request = scrapy.Request(url=blog_url, callback=self.parse_blog)
            request.meta['author'] = author
            request.meta['publication_date'] = publication_date
            request.meta['title'] = title
            request.meta['summary'] = summary
            request.meta['blog_url'] = blog_url
            
            yield request

        # follow pagination link
        current_url = article.xpath('//link[@rel="canonical"]/@href').extract_first()
        # last page of the blog
        next_url = article.xpath('//div[@class="archive-pagination pagination"]/ul/li[@class="pagination-next"]/a/@href').extract_first()
        # last_page = article.xpath('//div[@class="archive-pagination pagination"]/ul/li[last()-1]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)
            
           
    def parse_blog(self, response):
        author = response.meta['author']
        publication_date = response.meta['publication_date']
        title = response.meta['title']
        summary = response.meta['summary']
        blog_url = response.meta['blog_url']
        blog_content = response.xpath('normalize-space(//div[@class = "entry-content"])').extract()
        blog_headlines = response.xpath('//div[@class = "entry-content"]/h1/text()').extract()
        categories = response.xpath('//footer[@class = "entry-footer"]/p[@class="entry-meta"]/span[@class="entry-categories"]/a/text()').extract()
        tags = response.xpath('//footer[@class = "entry-footer"]/p[@class="entry-meta"]/span[@class="entry-tags"]/a/text()').extract()
        yield{
               'author': author,
               'publication_date': publication_date,
               'title': title,
               'summary': summary,
               'blog_url': blog_url,
               'blog_content': blog_content,
               'headlines': blog_headlines,
               'categories': categories,
               'tags': tags,
               }
