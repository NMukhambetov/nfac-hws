from aiohttp import web


movies = [
    { 'id': '1', 'title': 'The Shawshank Redemption', 'year': 1994, 'genre': 'Drama', 'rating': '4.95', },
    { 'id': '2', 'title': 'The Godfather', 'year': 1972, 'genre': 'Crime, Drama', 'rating': '4.88', },
    { 'id': '3', 'title': 'Inception', 'year': 2010, 'genre': 'Sci-Fi, Action', 'rating': '4.79', },
    { 'id': '4', 'title': 'Interstellar', 'year': 2014, 'genre': 'Sci-Fi, Drama', 'rating': '4.84', },
    { 'id': '5', 'title': 'Parasite', 'year': 2019, 'genre': 'Thriller, Drama', 'rating': '4.91', },
    { 'id': '6', 'title': 'The Dark Knight', 'year': 2008, 'genre': 'Action, Crime, Drama', 'rating': '4.89', },
    { 'id': '7', 'title': 'Pulp Fiction', 'year': 1994, 'genre': 'Crime, Drama', 'rating': '4.86', },
    { 'id': '8', 'title': 'The Lord of the Rings: The Return of the King', 'year': 2003, 'genre': 'Fantasy, Adventure', 'rating': '4.93', },
    { 'id': '9', 'title': 'Forrest Gump', 'year': 1994, 'genre': 'Drama, Romance', 'rating': '4.80', },
    { 'id': '10', 'title': 'Fight Club', 'year': 1999, 'genre': 'Drama, Thriller', 'rating': '4.78', },
]


async def handle(request):
    movies_json = dict(request.rel_url.query)
    res =filtered_movies(movies,**movies_json)
    return web.json_response ({'movies':res, 'filters':movies_json})

async def popular(request):
    sorted_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)
    movies_json = dict(request.rel_url.query)
    page = int(movies_json.pop('page',0))
    limit = int(movies_json.pop('limit',10))
    paginated_movies = paginate(sorted_movies, page, limit)
    return web.json_response({'movies': paginated_movies, 'paginate': movies_json})

def paginate(movies, page = 0, limit = 10):
    start = limit * page
    end = start + limit
    return movies[start:end]

def filtered_movies (movies,**filters):
    filtered_movies = []
    for movie in movies:
        match = True
        for key, value in filters.items():
            if str(movie.get(key)) != value:
                match = False
                break
        if match:
            filtered_movies.append(movie)
    return filtered_movies



app = web.Application()
app.add_routes([web.get('/', handle) , web.get('/popular',popular)])


if __name__ == '__main__':
    web.run_app(app, port=8080)