import scrapy
import json
import re
import urllib.request

from soupsieve.util import lower


class SensacineItemsSpider(scrapy.Spider):
    name = 'sensacine-items'
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
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=21',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=22',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=23',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=24',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=25',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=26',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=27',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=28',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=29',
        'https://www.sensacine.com/peliculas/mejores-peliculas/?page=30',
    ]

    # 30 paginations as entry points

    def parse(self, response):
        movie_hrefs = response.xpath('//a[@class="meta-title-link"]/@href').getall()

        for href in movie_hrefs:
            item_url = response.urljoin(href)
            yield scrapy.Request(item_url, callback=self.parse_movie)

    def parse_movie(self, response):
        # Exctracting json of structured data
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first(), strict=False)

        # Attributes o main object
        movie_title = data['name']
        movie_release_date = response.xpath('//div[@class="meta-body-item meta-body-info"]/span/text()').get()
        movie_runtime = data['duration']
        movie_genre = data['genre']
        movie_description = data['description']

        movie_title_without_special = re.sub('[^a-zA-Z0-9 \n\.]', '', movie_title)
        movie_title_normalized = lower(re.sub(' ', '-', movie_title_without_special))
        movie_image = '/movie_images/' + movie_title_normalized + '.jpg'

        # Images: getting data of image uploaded at sensacine
        image = data['image']['url']
        # Saving images from url to folder
        imgURL = image
        urllib.request.urlretrieve(imgURL, '/home/tgarcia/dev-projects/filmfy_scrap/filmfy_scrap/resources/movie_images/' + movie_title_normalized + '.jpg')
        # Setting local variable for DB

        movie_trailer = data['trailer']['url']

        # Saving actors if the movie have (due to animation ones)
        try:
            movie_actors = [item['name'] for item in data['actor']]
        except:
            movie_actors = ''

        # In case the is more than 1 director, dict type is evaluted first to just extract one or then loop
        if isinstance(data['director'], dict):
            movie_director = data['director']['name']
        else:
            movie_director = [item['name'] for item in data['director']]

        # Same as director but with movie creators
        try:
            if isinstance(data['creator'], dict):
                movie_creation = data['creator']['name']
            else:
                movie_creation = [item['name'] for item in data['creator']]
        except:
            movie_creation = ''

        # Printing information after scrap
        yield {
            'title': movie_title,
            'release_date': movie_release_date,
            'runtime': movie_runtime,
            'genre/s': movie_genre,
            'description': movie_description,
            'image': movie_image,
            'trailer': movie_trailer,
            'actors': movie_actors,
            'director': movie_director,
            'writers': movie_creation
        }
