from django.shortcuts import render
from django.http import HttpResponse

from web.models import Film 

# Create your views here.
def index(request):
    from web.models import Film
    
    films = Film.objects.all()
    context = {
        'films': films,
    }
    
    return render(request, 'web/index.html', context=context)

def film(request, id):
    film = Film.objects.get(pk=id)
    return render(request, 'web/film.html', {'film': film})