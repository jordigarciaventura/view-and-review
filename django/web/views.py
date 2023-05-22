
from django.db.models import Case, When, BooleanField
from typing import Any, Dict, Optional
from django.db import models
from django.db.models import Model, QuerySet
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden, QueryDict, JsonResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.models import User
from django.views import generic

from web.models import *
from web.forms import *

from . import api
import datetime

# Create your views here.

def mark_context_icons(context, user, list_keys):
    favlist   = Favlist.objects.filter(user=user)
    watchlist = Watchlist.objects.filter(user=user)
            
    for key in list_keys:
        if key not in context: continue
        for movie in context[key]:
            if favlist.exists() and favlist.filter(user=user, movie=movie['id']).exists():
                movie['favlist'] = True
            if watchlist.exists() and watchlist.filter(user=user, movie=movie['id']).exists():
                movie['watchlist'] = True


class UserView(generic.TemplateView):
    template_name = 'auth/profile.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        if not User.objects.filter(username=kwargs['username']).exists():
            return HttpResponseNotFound("User not found")
        
        profile_user = User.objects.filter(username=kwargs['username']).first()
        
        context['username'] = profile_user.username
        
        favlist = Favlist.objects.filter(user=profile_user).values('movie')
        if favlist.exists() and favlist.first()['movie']:
            favlist = list(map(lambda movie: api.movie(movie['movie']), favlist))
            context['favlist'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in favlist]
        
        watchlist = Watchlist.objects.filter(user=profile_user).values('movie')
        if watchlist.exists() and watchlist.first()['movie']:
            watchlist = list(map(lambda movie: api.movie(movie['movie']), watchlist))
            context['watchlist'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in watchlist]            

        if self.request.user.is_authenticated:          
            mark_context_icons(context, self.request.user, ['favlist', 'watchlist'])
        
        ratings = []
        user_ratings = Rating.objects.filter(user=profile_user).exclude(review=None)
        for user_rating in user_ratings:
            
            lists = {}
            if self.request.user.is_authenticated:
                # Add vote
                user_rating.review.user_vote = user_rating.review.user_vote(self.request.user)
                
                # Add watchlist and favlist
                logged_user = self.request.user
                if Favlist.objects.filter(user=logged_user, movie=user_rating.movie).exists():
                    lists['favlist'] = True
                if Watchlist.objects.filter(user=logged_user, movie=user_rating.movie).exists():
                    lists['watchlist'] = True
            
            movie_info = single_movie_preview_parser(api.movie(user_rating.movie.pk), poster_size="w342")
            
            result = {
                "rating": user_rating,
                "movie": dict(**movie_info, **lists)
            }
            ratings.append(result)
        
            context['user_ratings'] = ratings
        
        return context
    
    
class UserWatchlistView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Watch List"
    
        username = kwargs['username']
        watchlist = Watchlist.objects.filter(user__username=username).values('movie')
        if watchlist.exists() and watchlist.first()['movie']:
            watchlist = list(map(lambda movie: api.movie(movie['movie']), watchlist))
            context['movies'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in watchlist]            
                
        mark_context_icons(context, self.request.user, ['movies'])
    
        return context   

class UserFavlistView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Favorite List"
    
        username = kwargs['username']
        favlist = Favlist.objects.filter(user__username=username).values('movie')
        if favlist.exists() and favlist.first()['movie']:
            favlist = list(map(lambda movie: api.movie(movie['movie']), favlist))
            context['movies'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in favlist]            
                
        mark_context_icons(context, self.request.user, ['movies'])
    
        return context   

class IndexView(generic.TemplateView):
    template_name = "web/index.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        upcoming = api.upcoming()["results"]
        upcoming = movie_preview_parser(upcoming, poster_size="w342", count=10)
        context['upcoming'] = upcoming
        
        
        popular = api.popular()["results"]
        popular = movie_preview_parser(popular, poster_size="w342", count=10)
        context['popular'] = popular
    
        top_rated = api.top_rated()["results"]
        top_rated= movie_preview_parser(top_rated, poster_size="w342", count=10)
        context['top_rated'] = top_rated
        
        now_playing = api.now_playing()["results"]
        now_playing = movie_preview_parser(now_playing, poster_size="w342", count=10)
        context['now_playing'] = now_playing
        
        action = api.get_movies_by_genre_slug("action")["results"]
        action = movie_preview_parser(action, poster_size="w342", count=10)
        context['action'] = action
        
        animation = api.get_movies_by_genre_slug("animation")["results"]
        animation = movie_preview_parser(animation, poster_size="w342", count=10)
        context['animation'] = animation
        
        horror = api.get_movies_by_genre_slug("horror")["results"]
        horror = movie_preview_parser(horror, poster_size="w342", count=10)
        context['horror'] = horror
        
        if self.request.user.is_authenticated:
            mark_context_icons(context, self.request.user, ['upcoming', 'popular', 'top_rated', 'now_playing', 'action', 'animation', 'horror'])
        
        return context
    
class MovieView(generic.TemplateView):
    template_name = 'web/movie-section.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        # Get movie details
        movie_id = kwargs['pk']

        movie = api.movie(movie_id)           
        movie = movie_section_parser(movie)
        context['movie'] = movie
        
        # User Rating
        user_rating = None
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=self.request.user, movie=movie_id).first() or None
            context['user_rating'] = user_rating
        
        # Score
        score_count =  Rating.objects.filter(movie=movie_id).count()
        score_value = int(Rating.average(movie_id) * 20)
        
        context['score'] = {
            'value': score_value,
            'count': score_count,
            'source': 'V&R'
        }
        
        # Similar movies
        similar = api.get_similar(movie['id'])["results"]
        context['similar_movies'] = movie_preview_parser(similar, poster_size="w342", count=10)
    
        # Ratings
        ratings = Rating.objects.filter(movie=movie_id).exclude(review=None)
        if self.request.user.is_authenticated:
            ratings = ratings.exclude(user=self.request.user)
        context['ratings'] = ratings
        
        # Add rating user vote
        if self.request.user.is_authenticated:
            for rating in context['ratings']:
                rating.review.user_vote = rating.review.user_vote(self.request.user)
            if user_rating and user_rating.review:
                context['user_rating'].review.user_vote = context['user_rating'].review.user_vote(self.request.user)
    
        # Review form        
        if self.request.user.is_authenticated:
            if user_rating and user_rating.review:
                user_review = ReviewForm(user_rating.review.__dict__)
                context['review_form'] = user_review
            else:
                context['review_form'] = ReviewForm()
        
        return context

class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'
    
class ProfileSettingsView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'auth/profile_settings.html'
    login_url = 'login'
        

@require_http_methods(['POST', 'DELETE'])
def WatchlistView(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)
    
    data = QueryDict(request.body)
    user_watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
    movie = Movie.objects.get_or_create(tmdb_id=movie_id)[0]
    
    if request.method == 'POST':
        movie.save()
        user_watchlist.movie.add(movie_id)

    elif request.method == 'DELETE':
        user_watchlist.movie.remove(movie)

    return HttpResponse()

@require_http_methods(['POST', 'DELETE'])
def FavlistView(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)
    
    user_favlist = Favlist.objects.get_or_create(user=request.user)[0]
    movie = Movie.objects.get_or_create(tmdb_id=movie_id)[0]
        
    if request.method == 'POST':
        movie.save()
        user_favlist.movie.add(movie_id)
        print("Adding...")

    elif request.method == 'DELETE':
        user_favlist.movie.remove(movie)
        print("Removing...")

    return HttpResponse()

@require_http_methods(['POST', 'DELETE'])
def RatingView(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)

    data = QueryDict(request.body)
    movie, _ = Movie.objects.get_or_create(tmdb_id=movie_id)
    
    if request.method == 'POST':
        rating = data.get('rating')

        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"score": rating}
        )
        
    elif request.method == 'DELETE':    
        Rating.objects.filter(movie=movie, user=request.user).delete()

    # Score
    score_count =  Rating.objects.filter(movie=movie_id).count()
    score_value = int(Rating.average(movie_id) * 20)
    
    response = {
        'value': score_value,
        'count': score_count,
    }

    return JsonResponse(response)

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration succesful " + str(user))
            return redirect('/')
        messages.error(
            request, "Unsuccesful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name='registration/register.html', context={"form": form})


@require_http_methods(['POST', 'PUT', 'DELETE'])
def reviewVote(request):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)

    data = QueryDict(request.body)    
    review = Review.objects.get(pk=data.get('review'))
    vote = ReviewVote.objects.filter(user=request.user, review=review)
    value = data.get('value')
                
    if request.method == 'POST':
        if vote.exists():
            print(vote)
            if vote.value == value:
                return HttpResponse('Resource already exists', status=409)            
            vote.update(value=value)
        else:
            ReviewVote(user=request.user, review=review, value=data.get('value')=='true').save()

    elif request.method == 'PUT':
        new_value = data['value'] == 'true'
        vote.update(value=new_value)
    
    elif request.method == 'DELETE':
        vote.delete()
    
    return HttpResponse()


def userUpdateView(request):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)

    new_username = QueryDict(request.body).get('username')

    db_user = User.objects.filter(username=new_username)
    if db_user.exists():
        return HttpResponseForbidden("A user already has that username!")
    
    request.user.username = new_username
    request.user.save()
    return HttpResponse()


@require_http_methods(['GET', 'POST'])
def userDeleteView(request):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)
    
    if request.method == 'GET':
        return render(request=request, template_name='auth/user-confirm-delete.html', context={'object': request.user})
    elif request.method == 'POST':
        request.user.delete()
        return render(request=request, template_name='auth/user-deleted.html', context={'object': request.user})  

@require_http_methods(['POST', 'PUT', 'DELETE'])
def review(request, movie_id):
    if not request.user.is_authenticated:
        return HttpResponse(reverse('login'), status=401)
                
    related_rating = get_object_or_404(Rating, user=request.user, movie=movie_id)    
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)      
            if related_rating.review:
                return HttpResponse('Resource already exists', status=409)
            
            new_review.save()
            related_rating.review = new_review
            related_rating.review.save()
            related_rating.save()
            return HttpResponse(related_rating.review.id) 

    data = QueryDict(request.body)
        
    if request.method == 'DELETE':       
        related_rating.review.delete()
        related_rating.review = None
        
    elif request.method == 'PUT':
        related_rating.review.title = data.get('title')
        related_rating.review.content = data.get('content')
        related_rating.review.save()
    
    related_rating.save()
    return HttpResponse()               

def get_dict_keys(dict, keys):
    return {key:value for key, value in dict.items() if key in keys}

def single_movie_preview_parser(movie_result, poster_size="w92"):
    properties = ["title", "release_date", "id", "poster_path", "genres", "vote_average"]
    filtered_results = get_dict_keys(movie_result, properties)

    # Change poster path to url
    poster_path = filtered_results['poster_path']
    poster_url = api.get_image_url(poster_path, type="poster", size=poster_size)
    filtered_results['poster_path'] = poster_url
    
    # Change genre ids to names
    genre_ids = filtered_results['genres']
    genres = [api.get_genre_name(genre_id['id']) for genre_id in genre_ids]
    filtered_results['genres'] = genres
        
    # Get only the year from the release date
    filtered_results['release_date'] = filtered_results['release_date'][:4]
    
    # Get the score
    filtered_results['score'] = filtered_results['vote_average'] * 10
    filtered_results.pop('vote_average')

    return filtered_results

def movie_preview_parser(results, poster_size="w92", count=0):
    # Get only the properties we want
    properties = ["title", "release_date", "id", "poster_path", "genre_ids", "vote_average"]
    filtered_results = [get_dict_keys(result, properties) for result in results]
    
    # Check if all properties are not empty
    filtered_results = [result for result in filtered_results if all(result.values())]
    
    # Get only some results
    if count:
        filtered_results = filtered_results[:count]
    
    for i in range(len(filtered_results)):
        # Change poster path to url
        poster_path = filtered_results[i]['poster_path']
        poster_url = api.get_image_url(poster_path, type="poster", size=poster_size)
        filtered_results[i]['poster_path'] = poster_url
        
        # Change genre ids to names
        genre_ids = filtered_results[i]['genre_ids']
        genres = [api.get_genre_name(genre_id) for genre_id in genre_ids]
        filtered_results[i]['genres'] = genres
        filtered_results[i].pop('genre_ids')
            
        # Get only the year from the release date
        filtered_results[i]['release_date'] = filtered_results[i]['release_date'][:4]
        
        # Get the score
        filtered_results[i]['score'] = filtered_results[i]['vote_average'] * 10
        filtered_results[i].pop('vote_average')
        
    return filtered_results

def movie_section_parser(movie_details):
    # Get only the properties we want
    properties = ["backdrop_path", "genres", "id", "overview", "poster_path", "release_date", "runtime", "title", "vote_average", "vote_count"]
    filtered_details = get_dict_keys(movie_details, properties)

    # Change poster path to url
    poster_path = filtered_details['poster_path']
    filtered_details['poster'] = api.get_image_url(poster_path, type="poster", size="w500")
    filtered_details.pop('poster_path')

    # Change backdrop path to url
    backdrop_path = filtered_details['backdrop_path']
    filtered_details['cover'] = api.get_image_url(backdrop_path, type="backdrop", size="original")
    filtered_details.pop('backdrop_path')

    # Change genre ids to names
    genres = filtered_details['genres']
    genre_ids = [genre['id'] for genre in genres]
    genres = [api.get_genre_name(genre_id) for genre_id in genre_ids]
    filtered_details['genres'] = genres

    # Format the release date
    year, month, day = map(int, filtered_details['release_date'].split('-'))
    date = datetime.datetime(year, month, day).strftime("%Y, %b %d")
    filtered_details['release_date'] = date

    # Format runtime
    runtime = filtered_details['runtime']
    hours = runtime // 60
    minutes = runtime % 60
    filtered_details['runtime'] = f"{hours}h {minutes}m"
    
    # Format tmdb_score
    score_value = int(filtered_details['vote_average'] * 10)
    score_count = format_count(filtered_details['vote_count'])
    
    filtered_details['tmdb_score'] = {
        'value': score_value,
        'count': score_count,
        'source': 'TMDB'
    }
    
    filtered_details.pop('vote_average')
    filtered_details.pop('vote_count')            
    
    # Add credits
    cast = api.get_movie_credits(filtered_details['id'])
    filtered_details['directors'] = set(x['name'] for x in api.get_directors(cast))
    filtered_details['writers'] = set(x['name'] for x in api.get_writers(cast))
    properties = ['name', 'character', 'profile_path']
    filtered_details['actors'] = sorted([get_dict_keys(x, properties) for x in api.get_actors(cast)], key=lambda x: x['profile_path'] == None)
    for i in range(len(filtered_details['actors'])):
        # Change profile path to url
        profile_path = filtered_details['actors'][i]['profile_path']
        if profile_path:
            filtered_details['actors'][i]['profile_path'] = api.get_image_url(profile_path, type="profile", size="w185")
        else:
            filtered_details['actors'][i]['profile_path'] = ""

    return filtered_details

def format_count(count):
    if count > 1000000:
        return f"{count/1000000:.1f}M"
    if count > 1000:
        return f"{count/1000:.1f}K"
    return count

def trailer(request, movie_id):
    return HttpResponse(api.get_movie_trailer(movie_id))


class UpcomingView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Upcoming"
        
        movies = api.upcoming()["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context


class PopularView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Popular"
        
        movies = api.popular()["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
    
    
class TopRatedView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Top Rated"
        
        movies = api.top_rated()["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
    
class NowPlayingView(generic.TemplateView):
    template_name = 'web/list.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Now Playing"
        
        movies = api.now_playing()["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
    
class SimilarView(generic.TemplateView):
    template_name = 'web/list.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Similar movies"
        
        movies = api.get_similar(kwargs['movie_id'])["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
        
    
class GenreView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}        
        
        genre_id = api.get_genre_id(kwargs['genre'])
        genre_name = api.get_genre_name(genre_id)
        context['title'] = genre_name
        
        movies = api.get_movies_by_genre_id(genre_id)["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
    
class YearView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}                
        context['title'] = kwargs['year']
        
        movies = api.get_movies_by_year(kwargs['year'])["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context
    
class SearchView(generic.TemplateView):
    template_name = 'web/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        context['title'] = "Search results"
    
        query = self.request.GET.get('query')
        movies = api.search(query)["results"]
        context['movies'] = movie_preview_parser(movies, poster_size="w342")
        return context                

def search(request):  
    if not request.GET.get('term'):
        return HttpResponseNotFound()
    
    query = request.GET.get('term')
    movies = api.search(query)["results"]
    movies = movie_preview_parser(movies, poster_size="w92", count=10)
    
    return JsonResponse(movies, safe=False)