from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView, name='register'),
    path('film/<pk>/', views.FilmView.as_view(), name='film'),
    path('rating/<pk>/', views.rate, name='rating'),
    path('reputation/', views.reputation, name='reputation'),
    path('search/', views.search, name='search'),
]

urlpatterns += staticfiles_urlpatterns()