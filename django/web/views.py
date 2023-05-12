from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, QueryDict, JsonResponse
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.models import User
from django.views import generic

import requests
import os
import json

from web.models import Film, Rating, Reputation
from web.forms import RegisterForm, RatingForm, ReputationForm

from . import api


endpoint="https://api.themoviedb.org/3"
image_endpoint="https://image.tmdb.org/t/p"
api_key = os.environ.get('TMDB_BEARER_TOKEN', "")
headers = {"Authorization": f"Bearer {api_key}"}

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = "web/index.html"
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['popular'] = api.popular(number=20)
        context['latest'] = api.latest(number=20)
        context['top_films'] = api.top_most_rated(number=20)
        context['top_batfilms'] = api.top_most_rated_includes(includes="Batman")
        
        return context

class FilmView(generic.DetailView):
    template_name = 'web/film.html'
    model = Film

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(FilmView, self).get_context_data(**kwargs)
        context['film'] = self.get_object()
        context['RATING_CHOICES'] = Rating.RATING_CHOICES
        context['form'] = RatingForm(initial={'film': self.get_object()})
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=self.request.user, film=self.get_object()).first()
            if user_rating:
                context['form'] = RatingForm(instance=user_rating)
                context['user_rating'] = user_rating

        # Gets the form prefilled with the user's past choices
        return context

class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'


class ProfileView(generic.TemplateView):
    template_name = 'auth/profile.html'
    

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration succesful " + str(user))
            return redirect('/')
        messages.error(
            request, "Unsuccesful registration. Invalid information.")
    return render(request=request, template_name='registration/register.html', context={"form": form})

@login_required
@require_http_methods(["POST", "DELETE"])
def reputation(request):     
    if request.method == 'POST':   
        form = ReputationForm(request.POST)
        
        if form.is_valid():
            reputation = form.save(commit=False)
            old_reputation = Reputation.objects.filter(user=reputation.user, rating=reputation.rating)
            if old_reputation.exists():
                old_reputation.update(value=reputation.value)
            else:
                reputation.save()
    if request.method == 'DELETE':
        data = QueryDict(request.body)

        reputation = Reputation.objects.filter(user=data.get('user'), rating=data.get('rating'))
        reputation.delete()
    return HttpResponse()
            
@login_required
def userUpdateView(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        return HttpResponseForbidden("Cannot update other's account")

    username = QueryDict(request.body).get('username')

    db_user = User.objects.filter(username=username)
    if db_user.exists():
        return HttpResponseForbidden("A user already has that username!")
    
    user.username = username
    user.save()
    return HttpResponse()

class UserDeleteView(DeleteView):
    model = User
    
    def form_valid(self, form):
        self.object = self.get_object()
        if self.object == self.request.user:
            self.object.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseForbidden("Cannot delete other's account")

class RatingDeleteView(DeleteView):
    model = Rating

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseForbidden("Cannot delete other's posts")

    def get_success_url(self) -> str:
        return reverse('film', args=(self.object.film.pk,)) 
    

@login_required
def rate(request, pk):
    if request.method == "POST":    
        get_object_or_404(Film, pk=pk)
        
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
            return HttpResponseRedirect(reverse('film', args=(pk,)))
        else:
            messages.error(request, "Unsuccesful review. Invalid information: " + str(form.errors))
    if request.method == "DELETE":    
        data = QueryDict(request.body)

        rating = Rating.objects.filter(user=data.get('user'), film=data.get('film'))
        rating.delete()

    return HttpResponseRedirect(reverse('film', args=(pk,)))
               

def search(request):
    if 'term' in request.GET:
        payload = {"query": request.GET.get('term')}
        json_response = requests.get(endpoint + "/search/movie", headers=headers, params=payload).json()
        results = json_response["results"]
        
        filtered_results = [{prop: d[prop] for prop in ['title', 'release_date', 'vote_average', 'id', 'poster_path', 'genre_ids']} for d in results]
        filtered_results = [d for d in filtered_results if all(d.values())]
        filtered_results = filtered_results[:10]
        
        for i in range(len(filtered_results)):
            # Change poster path to url
            poster_path = filtered_results[i]['poster_path']
            poster_url = get_image_url(poster_path)
            filtered_results[i]['poster_path'] = poster_url
                
            # Change genre ids to names
            genre_ids = filtered_results[i]['genre_ids']
            genres = get_genres_names(genre_ids)
            filtered_results[i].pop('genre_ids')
            filtered_results[i]['genres'] = ", ".join(genres[:2])
                
            # Get only the year from the release date
            filtered_results[i]['release_date'] = filtered_results[i]['release_date'][:4]
                
        return JsonResponse(filtered_results, safe=False)
    return HttpResponse()


def get_image_url(path, width=92):
    return image_endpoint + f"/w{str(width)}" + path
    

def get_genres_names(ids):
    genres = { 
        "28": "Action",
        "12": "Adventure",
        "16": "Animation",
        "35": "Comedy",
        "80": "Crime",
        "99": "Documentary",
        "18": "Drama",
        "10751": "Family",
        "14": "Fantasy",
        "36": "History",
        "27": "Horror",
        "10402": "Music",
        "9648": "Mystery",
        "10749": "Romance",
        "878": "Sci-Fi",
        "10770": "TV Movie",
        "53": "Thriller",
        "10752": "War",
        "37": "Western"}
    
    return [genres[str(id)] for id in ids if str(id) in genres]