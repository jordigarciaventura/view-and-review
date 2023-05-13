from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView, name='register'),
    path('accounts/<pk>', views.ProfileView.as_view(), name='profile'),
    path('accounts/<pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('accounts/<pk>/update/', views.userUpdateView, name='user-update'),
    path('film/<pk>/', views.FilmView.as_view(), name='film'),
    path('rating/<film_id>/', views.rate, name='rating'),
    path('rating/<film_id>/delete/', views.ratingDelete, name='rating-delete'),
    path('reputation/', views.reputation, name='reputation'),
    path('search/', views.search, name='search'),
    path('section/<title>', views.section, name='section'),
    path('watchlist/<movie_id>', views.watchlist, name='watchlist'),
    path('favorite/<movie_id>', views.favorite, name='favorite'),
    path('trailer/<movie_id>', views.trailer, name='trailer'),
    path('movie/<pk>/', views.movie, name='movie'),
]

urlpatterns += staticfiles_urlpatterns()