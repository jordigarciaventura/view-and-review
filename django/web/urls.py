from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('movie/<pk>/', views.MovieView.as_view(), name='movie'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.LogoutView.as_view(), name='logout-page'),
    path('accounts/register/', views.RegisterView, name='register'),
    path('accounts/delete/', views.userDeleteView, name='user-delete'),
    path('accounts/update/', views.userUpdateView, name='user-update'),
    path('accounts/settings/', views.ProfileSettingsView.as_view(), name='user-settings'),
    path('accounts/<slug:username>/', views.UserView.as_view(), name='user-profile'),
    path('accounts/<slug:username>/watchlist', views.UserWatchlistView.as_view(), name='user-watchlist'),
    path('accounts/<slug:username>/favlist', views.UserFavlistView.as_view(), name='user-favlist'),
    
    path('search/', views.SearchView.as_view(), name='search'),
    path('search/json', views.search, name='json-search'),
    
    path('trailer/<movie_id>/', views.trailer, name='trailer'),    
    path('watchlist/<movie_id>/', views.WatchlistView, name='watchlist'),
    path('favlist/<movie_id>/', views.FavlistView, name='favlist'),  
    path('rating/<str:movie_id>/', views.RatingView, name='rating'),
    
    path('review/vote/', views.reviewVote, name='review-vote'),
    path('review/<movie_id>/', views.review, name='review'),
    
    path('list/upcoming', views.UpcomingView.as_view(), name='upcoming'),
    path('list/popular', views.PopularView.as_view(), name='popular'),
    path('list/top-rated', views.TopRatedView.as_view(), name='top-rated'),
    path('list/now-playing', views.NowPlayingView.as_view(), name='now-playing'),
    
    path('list/similar/<movie_id>', views.SimilarView.as_view(), name='similar'),
    path('list/genre/<slug:genre>/', views.GenreView.as_view(), name='genre'), 
    path('list/year/<int:year>/', views.YearView.as_view(), name='year'),    
]

urlpatterns += staticfiles_urlpatterns()