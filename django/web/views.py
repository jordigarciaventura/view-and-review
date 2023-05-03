from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
        context['film'] = self.get_object()
        context['RATING_CHOICES'] = Rating.RATING_CHOICES
        context['form'] = RatingForm(initial={'film': self.get_object()})
        if self.request.user.is_authenticated:
            user_ratings = Rating.objects.filter(user=self.request.user)
            if user_ratings:
                user_film_rating = user_ratings.get(film=self.get_object())
                context['form'] = RatingForm(instance=user_film_rating)

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

@login_required
def rate(request, pk):
    if request.method == "POST":    
        film = get_object_or_404(Film, pk=pk)
        
        form = RatingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['film'])
            # Process the data in form.cleaned_data
            rating = form.save(commit=False)
            rating.user = User.objects.get(username=request.user)
            old_rating = Rating.objects.filter(user=rating.user)
            print(rating.film)
            if old_rating.exists():
                old_rating.update(score=rating.score, review=rating.review, review_title=rating.review_title)
            else:
                rating.save()
            return HttpResponseRedirect(reverse('film', args=(pk,)))
        else:
            messages.error(request, "Unsuccesful review. Invalid information: " + str(form.errors))

    return HttpResponseRedirect(reverse('film', args=(pk,)))
               
    