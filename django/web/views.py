from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.views import generic

from web.models import Film, Rating
from web.forms import RegisterForm, RatingForm

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = "web/index.html"


class FilmView(generic.DetailView):
    template_name = 'web/film.html'
    model = Film

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(FilmView, self).get_context_data(**kwargs)
        user_ratings = Rating.objects.filter(user=self.request.user)
        context['film'] = self.get_object()
        if user_ratings:
            user_film_rating = user_ratings.get(film=self.get_object())
            context['form'] = RatingForm(instance=user_film_rating)
        else:
            context['form'] = RatingForm()

        # Gets the form prefilled with the user's past choices
        return context


class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'


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


class RatingView(FormView):
    template_name = "web/film.html"
    form_class = RatingForm
    
    def form_invalid(self, form):
        return HttpResponse("Invalid form!")
        
    def form_valid(self, form):        
        # Method called when valid form data is POSTED
        rating = form.save(commit=False)
        rating.user = User.objects.get(username=self.request.user)
        old_rating = Rating.objects.filter(user=rating.user)
        if old_rating.exists():
            # If there is already a rating from this user for this film, update the rating instead of creating a new one
            old_rating.update(score=rating.score)
        else:
            rating.save()
            
        self.success_url = self.request.META['HTTP_REFERER']
        return super(RatingView, self).form_valid(form)
