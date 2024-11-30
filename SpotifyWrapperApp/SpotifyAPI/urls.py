from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.spotify_login, name='spotify-login'),
    path('callback/', views.spotify_callback, name='spotify-callback'),
    path('top-artists/', views.user_top_artists, name='user-top-artists'),
    path('top-tracks/', views.user_top_tracks, name='user-top-tracks'),
]