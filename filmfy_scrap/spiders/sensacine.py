# helper: https://www.geeksforgeeks.org/how-to-follow-links-with-python-scrapy/

import scrapy


class SensacineSpider(scrapy.Spider):
    name = 'sensacine'
    allowed_domains = ['sensacine.com']
    start_urls = [
        'https://www.sensacine.com/peliculas/mejores-peliculas/',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=2',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=3',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=4',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=5'
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=6',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=7',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=8',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=9',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=10',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=11',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=12',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=13',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=14',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=15',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=16',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=17',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=18',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=19',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=20',
    ]

    def parse(self, response):
        content = response.xpath('//div[@class="gd-col-middle"]/ol/li')

        for card in content:
            banned_card_keywords = ['mobile-referrer-atf', 'mobile-referrer-mtf', 'mobile-referrer-btf']
            if not card.xpath('.//div/@id').get() in banned_card_keywords:
                movie_title = card.xpath('.//div/div[1]/h2/a[@class="meta-title-link"]/text()').get()
                movie_description = card.xpath('.//div[@class="synopsis"]/div/text()').getall()
                movie_genres = card.xpath('.//div[@class="meta-body-item meta-body-info"]/a[@class="xXx"]/text()').getall()
                movie_runtime = card.xpath('.//div[@class="meta-body-item meta-body-info"]/text()').extract_first()
                movie_actors = card.xpath('.//div[@class="meta-body-item meta-body-actor"]/a/text()').getall()
                movie_direction = card.xpath('.//div[@class="meta-body-item meta-body-direction"]/a/text()').getall()

                yield {
                    'movie': movie_title,
                    'description': movie_description,
                    'genre/s': movie_genres,
                    'runtime': movie_runtime,
                    'actors': movie_actors,
                    'director/s': movie_direction
                }

        # next_page = response.selector.xpath('//div[@class="pagination-item-holder"]/span[@class="button button-md item current-item"]/following-sibling::a/@href').extract_first()
        # print(response.xpath('//@href').getall())
        # print(next_page)
        # next_page_url = response.urljoin(next_page)
        # print(next_page_url)
        # yield scrapy.Request(next_page_url)
