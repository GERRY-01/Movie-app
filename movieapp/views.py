from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    api_key = '07faedb9c6d062cd3deeb29fe4c16559'
    search_url = 'https://api.themoviedb.org/3/search/multi'
    image_base_url = 'https://image.tmdb.org/t/p/w500'
    trending_url = 'https://api.themoviedb.org/3/trending/movie/week'
    top_rated_url = 'https://api.themoviedb.org/3/movie/top_rated'

    #trending movies
    response = requests.get(trending_url, params={'api_key': api_key})
    trending_data = response.json().get('results', [])
    trending_movies = []

    if response.status_code == 200:
        for movie in trending_data:
            trending_movies.append({
                'title': movie.get('title'),
                'poster_url': f"{image_base_url}{movie['poster_path']}",
                'rating': movie.get('vote_average','N/A')
            })
    
    #top rated 
    top_rated_response = requests.get(top_rated_url, params={'api_key': api_key})
    top_rated_data = top_rated_response.json().get('results', [])
    top_rated_movies = []

    if top_rated_response.status_code == 200:
        for movie in top_rated_data:
            id = movie.get('id')
            title = movie.get('title')
            poster_url = f"{image_base_url}{movie['poster_path']}"
            rating = movie.get('vote_average','N/A')
            details_url = f"https://api.themoviedb.org/3/movie/{id}"
            details_response = requests.get(details_url, params={'api_key': api_key})
            details_data = details_response.json()
            imdb_id = details_data.get('imdb_id')

            top_rated_movies.append({
                'id': id,
                'title': title,
                'poster_url': poster_url,
                'rating': rating,
                'stream_url': f"https://vidsrc.to/embed/movie/{imdb_id}" if imdb_id else None
            })
            
    movie_data = None
    episodes_data = None

    if request.method == 'GET':
        query = request.GET.get('q')
        season_number = request.GET.get('season')
        selected_season = int(season_number) if season_number else None

        if query:
            # Search both movies and series
            params = {'api_key': api_key, 'query': query}
            response = requests.get(search_url, params=params)
            results = response.json().get('results', [])
            valid_results = [r for r in results if r['media_type'] in ['movie', 'tv']]

            if valid_results:
                media = valid_results[0]
                media_type = media['media_type']
                media_id = media['id']
                title = media.get('title') if media_type == 'movie' else media.get('name')
                overview = media.get('overview', 'No description available.')
                poster_path = media.get('poster_path')
                poster_url = f"{image_base_url}{poster_path}" if poster_path else None

                details_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}"
                details_response = requests.get(details_url, params={'api_key': api_key})
                details_data = details_response.json()

                if media_type == 'tv':
                    # get IMDb ID for TV show from /tv/{id}/external_ids
                    external_ids_url = f"https://api.themoviedb.org/3/tv/{media_id}/external_ids"
                    external_ids_response = requests.get(external_ids_url, params={'api_key': api_key})
                    external_ids_data = external_ids_response.json()
                    imdb_id = external_ids_data.get('imdb_id', '')
                else:
                    imdb_id = details_data.get('imdb_id', '')

                stream_url = f"https://vidsrc.to/embed/{media_type}/{imdb_id}" if imdb_id else None

                # Build movie_data
                movie_data = {
                    'title': title,
                    'overview': overview,
                    'poster_url': poster_url,
                    'stream_url': stream_url,
                    'media_type': media_type,
                    'imdb_id': imdb_id,
                    'seasons': []
                }

                # If it's a TV show, get seasons
                if media_type == 'tv':
                    total_seasons = details_data.get('number_of_seasons', 0)
                    movie_data['seasons'] = list(range(1, total_seasons + 1))

                    # If a season is selected, get its episodes
                    if selected_season:
                        season_url = f"https://api.themoviedb.org/3/tv/{media_id}/season/{selected_season}"
                        season_response = requests.get(season_url, params={'api_key': api_key})
                        season_data = season_response.json()
                        episodes_data = season_data.get('episodes', [])
                    
    

    return render(request, 'index.html', {
        'movie': movie_data,
        'episodes': episodes_data,
        'selected_season': selected_season,
        'trending_movies': trending_movies,
        'top_rated_movies': top_rated_movies
    })
