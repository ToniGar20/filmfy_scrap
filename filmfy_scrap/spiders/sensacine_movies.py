import requests_html
import scrapy
import json
import re
import urllib.request
from soupsieve.util import lower
from filmfy_scrap.spiders.resources.youtube_trailers import find_trailer


def start_session():
    session = requests_html.HTMLSession()
    return session


spider_session = start_session()


class SensacineMoviesSpider(scrapy.Spider):
    name = 'sensacine-movies'
    allowed_domains = ['sensacine.com']
    start_urls = [
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=2',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=3',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=4',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=5',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=6',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=7',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=8',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=9',
        # 'https://www.sensacine.com/peliculas/en-cartelera/cines/?page=10',

        'https://www.sensacine.com/peliculas/estrenos/mas-esperadas/',
        # 'https://www.sensacine.com/peliculas/estrenos/mas-esperadas/?page=2',
        # 'https://www.sensacine.com/peliculas/estrenos/mas-esperadas/?page=3',
        # 'https://www.sensacine.com/peliculas/estrenos/mas-esperadas/?page=4',
        # 'https://www.sensacine.com/peliculas/estrenos/mas-esperadas/?page=5',
    ]

    def parse(self, response):
        movie_hrefs = response.xpath('//a[@class="meta-title-link"]/@href').getall()

        for href in movie_hrefs:
            item_url = response.urljoin(href)
            yield scrapy.Request(item_url, callback=self.parse_movie)

    def parse_movie(self, response):
        # Extracting JSON of structured data
        data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first(), strict=False)

        # Attributes o main object
        movie_title = data['name']
        movie_release_date = response.xpath('//div[@class="meta-body-item meta-body-info"]/span/text()').get()

        try:
            movie_runtime = data['duration']
        except:
            movie_runtime = None

        movie_genre = data['genre']
        movie_description = data['description']

        movie_title_without_special = re.sub('[^a-zA-Z0-9 \n\.]', '', movie_title)
        movie_title_normalized = lower(re.sub(' ', '-', movie_title_without_special))
        movie_image = '/movies_images/' + movie_title_normalized + '.jpg'

        # Images: getting data of image uploaded at sensacine
        image = data['image']['url']
        # Saving images from url to folder
        img_url = image
        urllib.request.urlretrieve(img_url,
                                   'C:/Users/Toni/dev/filmfy_scrap/filmfy_scrap/img/' + movie_title_normalized + '.png')
        # Setting local variable for DB

        # Searching movie trailer at YouTube
        movie_trailer = find_trailer(spider_session, movie_title)

        # Saving actors if the movie have (due to animation ones)
        try:
            movie_actors = [item['name'] for item in data['actor']]
        except:
            movie_actors = ''

        # In case the is more than 1 director, dict type is evaluated first to just extract one or then loop
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
