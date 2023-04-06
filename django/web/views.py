from django.shortcuts import render
from django.views import generic

from web.models import Film 

# Create your views here.
def index(request): 
    films = Film.objects.all()[:5]
    context = {
        'films': films,
    }
    
    return render(request, 'web/index.html', context=context)

class FilmView(generic.DetailView):
    template_name = 'web/film.html'    
    model = Film
    
class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'