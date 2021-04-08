import scrapy
from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FatosSpider(CrawlSpider):
    name = 'fatos'
    allowed_domains = ['www.aosfatos.org']
    start_urls = ['http://www.aosfatos.org/']
    rules= (
        Rule(
            LinkExtractor(restrict_xpaths=('//nav//ul//li//a[re:test(@href, "checamos")]'))
        ),
        Rule(
            LinkExtractor(restrict_xpaths='/html/body/main/section/div/section/div/a'),
            callback='parse_new'
        ),
        Rule(
            LinkExtractor(restrict_css=('.pagination a'))
        )


    )

    def parse_new(self, response, **kwargs):
        title=response.xpath('/html/body/main/section/article/h1/text()').get()
        date= ' '.join(response.css('p.publish_date::text').get().split())
        #status=['Verdadeiro' if 'verdadeiro.png' in i.split('/') else 'Falso' for i in response.xpath('/html/body/main/section/article/p[@class="inline-stamp"]/img/@src').getall()]
        #quotes=response.xpath('//blockquote/p')
        quotes = response.css('article blockquote p')
        for quote in quotes:
            quote_text= quote.xpath('text()').get()
            #Encontrando os status referentes ao blockquote e substituindo espaços por ""
            status = quote.xpath('.//parent::blockquote/preceding-sibling::figure//figcaption//text()').getall()[-1]
            #x = [i.replace("\r\n", "") for i in quotes.xpath('./parent::blockquote/preceding-sibling::figure//figcaption//text()').getall()]
            #removendo ''

            yield {
                'title':title,
                'date': date,
                'url': response.url,
                'quote':quote_text,
                'status':status
            }
