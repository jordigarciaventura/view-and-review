from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<id>', views.film, name='film'),
    # path('accounts/', include())
]