YOUTUBE = 'https://www.youtube.com/embed'
YOUTUBE_SEARCH = 'https://www.youtube.com/results?search_query='


def find_trailer(session, movie):

    url_queried = YOUTUBE_SEARCH + movie + ' trailer'
    r = session.get(url_queried)
    r.html.render(sleep=4, timeout=5)

    movie_trailer = r.html.xpath('(//a[@id="video-title"])[1]/@href')
    movie_trailer_url = YOUTUBE + movie_trailer[0]

    return movie_trailer_url
