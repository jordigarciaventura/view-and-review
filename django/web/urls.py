from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView, name='register'),
    path('accounts/<slug>/', views.UserView.as_view(), name='profile'),
    path('accounts/<pk>/settings/', views.ProfileSettingsView.as_view(), name='profile-settings'),
    path('accounts/<pk>/settings/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('accounts/<pk>/settings/update/', views.userUpdateView, name='user-update'),
    
    path('rating/<film_id>/', views.rate, name='rating'),
    path('rating/<film_id>/delete/', views.ratingDelete, name='rating-delete'),
    path('reputation/', views.reputation, name='reputation'),
    path('search/', views.search, name='search'),
    path('section/<title>', views.section, name='section'),
    path('trailer/<movie_id>', views.trailer, name='trailer'),
    
    path('movie/<pk>/', views.MovieView.as_view(), name='movie'),
    path('watchlist/', views.WatchlistView, name='watchlist'),
    path('favlist/', views.FavlistView, name='favlist'),
]

urlpatterns += staticfiles_urlpatterns()