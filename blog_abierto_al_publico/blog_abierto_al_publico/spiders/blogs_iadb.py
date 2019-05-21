import scrapy
from scrapy import Request
from datetime import datetime
from dateutil import parser
from blog_abierto_al_publico.LanguageDetector import LanguageDetector
# import pdb
# import mymodule
# import locale

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
        articles = response.xpath('//article')

        for article in articles:
            author = article.xpath('header[@class="entry-header"]/p[@class="entry-meta"]/a/text()').extract_first(default='')
            publication_date = article.xpath('header[@class="entry-header"]/p[@class="entry-meta"]/time[@class="entry-time"]/@datetime').extract_first(default='')
            publication_date = parser.parse(publication_date[0:-6])
            publication_date = publication_date.strftime("%Y-%m-%dT%H:%M:%S%z") + publication_date.strftime('.%f')[:4] + 'Z'
            # pdb.set_trace()
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

        current_url = article.xpath('//link[@rel="canonical"]/@href').extract_first()
        # next page of the blog
        next_url = article.xpath('//div[@class="archive-pagination pagination"]/ul/li[@class="pagination-next"]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)
            
           
    def parse_blog(self, response):
        author = response.meta['author']
        publication_date = response.meta['publication_date']
        title = response.meta['title']
        summary = response.meta['summary']
        blog_url = response.meta['blog_url']
        blog_content = response.xpath('normalize-space(//div[@class = "entry-content"])').extract()
        lang = ''

        lang_det = LanguageDetector()    
        lang = lang_det.detect(str(blog_content))
        

        blog_headlines = response.xpath('//div[@class = "entry-content"]/h1/text()').extract()
        categories = response.xpath('//footer[@class = "entry-footer"]/p[@class="entry-meta"]/span[@class="entry-categories"]/a/text()').extract()
        tags = response.xpath('//footer[@class = "entry-footer"]/p[@class="entry-meta"]/span[@class="entry-tags"]/a/text()').extract()
        yield{
               'type': 'blog-post',
               'source': blog_url,
               'sensitivity': 'public',
               'employeeID': '',
               'sourceDate': publication_date,
               'generatedDate':'',
               'tags': tags,
               'author': author,
               'title': title,
               'summary': summary,
               'blog_content': blog_content,
               'headlines': blog_headlines,
               'categories': categories,
               'lang': lang,
               }
