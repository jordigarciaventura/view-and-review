
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
    favlist = Favlist.objects.filter(user=user)
    watchlist = Watchlist.objects.filter(user=user)
            
    for key in list_keys:
        if key not in context: continue
        for movie in context[key]:
            if favlist.exists() and favlist.filter(user=user, movie=movie['id']).exists():
                movie['favlist'] = 1
            if watchlist.exists() and watchlist.filter(user=user, movie=movie['id']).exists():
                movie['watchlist'] = 1
            

class UserView(generic.TemplateView):
    template_name = 'auth/profile.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = User.objects.filter(username=kwargs['username']).first()

        context['username'] = user.username
        
        favlist = Favlist.objects.filter(user=user).values('movie')
        if favlist.exists() and favlist.first()['movie']:
            favlist = list(map(lambda movie: api.movie(movie['movie']), favlist))
            context['favlist'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in favlist]
        
        watchlist = Watchlist.objects.filter(user=user).values('movie')
        if watchlist.exists() and watchlist.first()['movie']:
            watchlist = list(map(lambda movie: api.movie(movie['movie']), watchlist))
            context['watchlist'] = [single_movie_preview_parser(movie_detail, poster_size="w342") for movie_detail in watchlist]            
        
        mark_context_icons(context, self.request.user, ['favlist', 'watchlist'])
        
        user_ratings = Rating.objects.filter(user=user)
        context['ratings'] = [rating for rating in user_ratings if rating.review]
                
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
        
        latest = api.latest()["results"]
        latest = movie_preview_parser(latest, poster_size="w342", count=10)
        context['latest'] = latest
        
        if self.request.user.is_authenticated:
            mark_context_icons(context, self.request.user, ['latest', 'top_rated', 'popular', 'upcoming'])
        
        return context
    
class MovieView(generic.TemplateView):
    template_name = 'web/movie-section.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = {}
        # Can raise 404
        movie_id = kwargs['pk']
        movie = api.movie(movie_id)           
        movie = movie_section_parser(movie)
                
        context['movie'] = movie
        
        context['RATING_CHOICES'] = Rating.RATING_CHOICES
        context['ratings'] = Rating.objects.filter(movie=movie_id).exclude(review=None)
        
        if self.request.user.is_authenticated:
            context['ratings'] = context['ratings'].exclude(user=self.request.user)
            context['user_rating'] = Rating.objects.filter(user=self.request.user, movie=movie_id).first()

        # Gets the form prefilled with the user's past choices
        return context

class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'
    
class ProfileSettingsView(generic.TemplateView, LoginRequiredMixin):
    template_name = 'auth/profile_settings.html'
    login_url = 'login'
        

@require_http_methods(['POST', 'DELETE'])
def WatchlistView(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    
    data = QueryDict(request.body)
    user_watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
    movie = Movie.objects.get_or_create(tmdb_id=data.get('movie_id'))[0]
    
    if request.method == 'POST':
        movie.save()
        user_watchlist.movie.add(data.get('movie_id'))

    elif request.method == 'DELETE':
        user_watchlist.movie.remove(movie)

    return HttpResponse()

@require_http_methods(['POST', 'DELETE'])
def FavlistView(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    
    data = QueryDict(request.body)
    user_favlist = Favlist.objects.get_or_create(user=request.user)[0]
    movie = Movie.objects.get_or_create(tmdb_id=data.get('movie_id'))[0]
    
    if request.method == 'POST':
        movie.save()
        user_favlist.movie.add(data.get('movie_id'))

    elif request.method == 'DELETE':
        user_favlist.movie.remove(movie)

    return HttpResponse()

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # MyProfile.create(user).save()
            login(request, user)
            messages.success(request, "Registration succesful " + str(user))
            return redirect('/')
        messages.error(
            request, "Unsuccesful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name='registration/register.html', context={"form": form})

@login_required
@require_http_methods(['POST', 'DELETE', 'PUT'])
def reputation(request):     
    if request.method == 'POST':   
        form = ReputationForm(request.POST)
        if form.is_valid():
            form.save()
    if request.method == 'PUT':   
        data = QueryDict(request.body)
        new_value = data.get('value') == 'true'
        Reputation.objects.filter(user=data.get('user'), rating=data.get('rating')).update(value=new_value)
    if request.method == 'DELETE':
        data = QueryDict(request.body)
        Reputation.objects.filter(user=data.get('user'), rating=data.get('rating')).delete()
    return HttpResponse()
            
def userUpdateView(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

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
        return HttpResponse('Unauthorized', status=401)
    
    if request.method == 'GET':
        return render(request=request, template_name='auth/user-confirm-delete.html', context={'object': request.user})
    elif request.method == 'POST':
        request.user.delete()
        return render(request=request, template_name='auth/user-deleted.html', context={'object': request.user})


@login_required
@require_http_methods(['GET', 'POST'])
def ratingDelete(request, film_id):
    object = Rating.objects.filter(film=film_id, user=request.user).first()
    if request.method == 'GET':
        return render(request=request, template_name='web/rating_confirm_delete.html', context={'object': object})
        
    # POST request logic
    object.delete()
    return HttpResponseRedirect(reverse('film', args=(film_id)))    

@login_required
@require_http_methods(['POST'])
def rate(request, film_id):
    form = RatingForm(request.POST)
    if form.is_valid():
        # Process the data in form.cleaned_data
        rating = form.save(commit=False)
        rating.user = User.objects.get(username=request.user)
        old_rating = Rating.objects.filter(user=rating.user)
        if old_rating.exists():
            old_rating.update(score=rating.score, review=rating.review, review_title=rating.review_title)
        else:
            rating.save()
        return HttpResponseRedirect(reverse('film', args=(film_id,)))
    else:
        messages.error(request, "Unsuccesful review. Invalid information: " + str(form.errors))
    
        if form.is_valid():
            # Process the data in form.cleaned_data
            rating = form.save(commit=False)
            rating.user = User.objects.get(username=request.user)
            old_rating = Rating.objects.filter(user=rating.user)
            if old_rating.exists():
                old_rating.update(score=rating.score, review=rating.review, review_title=rating.review_title)
            else:
                rating.save()
            return HttpResponseRedirect(reverse('film', args=(pk,)))
        else:
            messages.error(request, "Unsuccesful review. Invalid information: " + str(form.errors))
    if request.method == "DELETE":    
        data = QueryDict(request.body)

        rating = Rating.objects.filter(user=data.get('user'), film=data.get('film'))
        rating.delete()

    return HttpResponseRedirect(reverse('film', args=(pk,)))
               

def get_dict_keys(dict, keys):
    return {key:value for key, value in dict.items() if key in keys}

def search(request):
    if 'term' in request.GET:
        query = request.GET.get('term')
        results = api.search(query)["results"]
        
        filtered_results = movie_preview_parser(results, poster_size="w92", count=10)
                
        return JsonResponse(filtered_results, safe=False)
    return HttpResponse()

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
    filtered_results['genres'] = ", ".join(genres[:2])
        
    # Get only the year from the release date
    filtered_results['release_date'] = filtered_results['release_date'][:4]
    
    # Get the score
    filtered_results['score'] = filtered_results['vote_average'] * 10
    filtered_results.pop('vote_average')

    return filtered_results

def movie_preview_parser(results, poster_size="w92", count=10):
    # Get only the properties we want
    properties = ["title", "release_date", "id", "poster_path", "genre_ids", "vote_average"]
    filtered_results = [get_dict_keys(result, properties) for result in results]
    
    # Check if all properties are not empty
    filtered_results = [result for result in filtered_results if all(result.values())]
    
    # Get only some results
    filtered_results = filtered_results[:count]
    
    for i in range(len(filtered_results)):
        # Change poster path to url
        poster_path = filtered_results[i]['poster_path']
        poster_url = api.get_image_url(poster_path, type="poster", size=poster_size)
        filtered_results[i]['poster_path'] = poster_url
        
        # Change genre ids to names
        genre_ids = filtered_results[i]['genre_ids']
        genres = [api.get_genre_name(genre_id) for genre_id in genre_ids]
        filtered_results[i]['genres'] = ", ".join(genres[:2])
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
    filtered_details['poster_path'] = api.get_image_url(poster_path, type="poster", size="w500")

    # Change backdrop path to url
    backdrop_path = filtered_details['backdrop_path']
    filtered_details['backdrop_path'] = api.get_image_url(backdrop_path, type="backdrop", size="w1280")

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
    
    # Format vote average
    filtered_details['vote_average'] = int(filtered_details['vote_average'] * 10)
    
    # Add credits
    cast = api.get_movie_credits(filtered_details['id'])
    filtered_details['directors'] = set(x['name'] for x in api.get_directors(cast))
    filtered_details['writers'] = set(x['name'] for x in api.get_writers(cast))
    properties = ['name', 'character', 'profile_path']
    filtered_details['actors'] = [get_dict_keys(x, properties) for x in api.get_actors(cast)]
    for i in range(len(filtered_details['actors'])):
        # Change profile path to url
        profile_path = filtered_details['actors'][i]['profile_path']
        filtered_details['actors'][i]['profile_path'] = api.get_image_url(profile_path, type="profile", size="w185")

    return filtered_details

def section(request, title):
    print(title)
    return HttpResponse()

def trailer(request, movie_id):
    trailer = api.get_movie_trailer(movie_id)
    return HttpResponse(trailer)