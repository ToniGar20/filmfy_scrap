
import scrapy

# https://gist.github.com/1060460048/40b8734bb26e37c7b7e7cabfde29ae21

class FilmaffinitySpider(scrapy.Spider):
    name = 'filmaffinity'
    allowed_domains = ['filmaffinity.com']
    start_urls = ['https://www.filmaffinity.com/es/topgen.php?genres=-DO&chv=1&orderby=avg&movietype=serie%7Conly-serie&country=&fromyear=1874&toyear=2021&ratingcount=3&runtimemin=0&runtimemax=4']

    def parse(self, response):
        content_links = response.xpath('//*[@id="top-movies"]/li/a/@href').getall()
        for link in content_links:
            yield scrapy.Request(link, callback=self.parse_details)

    def parse_details(self, response):
        title = response.xpath('//h1/span/text()').get()
        description = response.xpath('//*[@id="left-column"]/dl[1]/dd[13]/text()').get()
        release_year = response.xpath('//*[@id="left-column"]/dl[1]/dd[3]/text()').get()
        runtime = response.xpath('//*[@id="left-column"]/dl[1]/dd[4]/text()').get()
        country = response.xpath('//*[@id="left-column"]/dl[1]/dd[5]/text()').get()
        genres = response.xpath('//*[@id="left-column"]/dl[1]/dd[11]/a/text()').get()

        yield {
            'title': title,
            'description': description,
            'year': release_year,
            'runtime': runtime,
            'country': country,
            'genre/s': genres,
        }
