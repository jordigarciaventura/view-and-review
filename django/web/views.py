from django.shortcuts import render, redirect
from django.views import generic

from web.models import Film 

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "web/index.html"

class FilmView(generic.DetailView):
    template_name = 'web/film.html'    
    model = Film
    
class LogoutView(generic.TemplateView):
    template_name = 'registration/logout.html'
    
from django.contrib.auth import login    
from web.forms import RegisterForm
from django.contrib import messages

def RegisterView(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration succesful " + str(user))
            return redirect('/')
        messages.error(request, "Unsuccesful registration. Invalid information.")
    return render(request=request, template_name='registration/register.html', context={"form": form})