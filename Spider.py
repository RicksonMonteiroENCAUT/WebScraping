import scrapy

class AosFatosSpider(scrapy.Spider):
    name='aos_fatos'
    start_urls=['https://www.aosfatos.org/']#Atalho para função start_url que realiza um request para cada url, em seguida chama sua função de callback(parse)
    #navega pelo menu e abre cada seção
    def parse(self, response, **kwargs):
        links = response.xpath('//nav//ul//li//a[re:test(@href, "checamos")]/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_category
            )
    #
    def parse_category(self, response):
        news = response.xpath('/html/body/main/section/div/section/div/a/@href').getall()
        for new_url in news:
            yield scrapy.Request(url=response.urljoin(new_url), callback=self.parse_new)

        pages_url= response.css('.pagination a::attr(href)').getall()
        for page in pages_url:
            yield scrapy.Request(
                url=response.urljoin(page),
                callback= self.parse_category
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

