from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden, QueryDict
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.contrib.auth.models import User
from django.views import generic

from web.models import Film, Rating, Reputation
from web.forms import RegisterForm, RatingForm, ReputationForm

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = "web/index.html"


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
    template_name = 'profile.html'
    

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
        print("Got deletee!!!")
        
        data = QueryDict(request.body)

        rating = Rating.objects.filter(user=data.get('user'), film=data.get('film'))
        rating.delete()

    return HttpResponseRedirect(reverse('film', args=(pk,)))
    