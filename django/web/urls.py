from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView, name='register'),
    path('accounts/settings/', views.ProfileSettingsView.as_view(), name='user-settings'),
    path('accounts/delete/', views.userDeleteView, name='user-delete'),
    path('accounts/update/', views.userUpdateView, name='user-update'),
    path('accounts/<slug:username>/', views.UserView.as_view(), name='user-profile'),
    
    path('rating/<film_id>/delete/', views.ratingDelete, name='rating-delete'),
    path('review/<movie_id>/', views.review, name='review'),
    path('review/vote/', views.reviewVote, name='review-vote'),
    path('search/', views.search, name='search'),
    path('section/<title>', views.section, name='section'),
    path('trailer/<movie_id>', views.trailer, name='trailer'),
    
    path('movie/<pk>/', views.MovieView.as_view(), name='movie'),
    path('watchlist/', views.WatchlistView, name='watchlist'),
    path('favlist/', views.FavlistView, name='favlist'),
    path('rating/', views.RatingView, name='rating'),
]

urlpatterns += staticfiles_urlpatterns()