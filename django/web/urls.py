from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<pk>', views.FilmView.as_view(), name='film'),
    path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += staticfiles_urlpatterns()