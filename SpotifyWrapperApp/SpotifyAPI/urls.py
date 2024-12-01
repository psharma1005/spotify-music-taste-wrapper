from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.spotify_login, name='spotify-login'),
    path('callback/', views.spotify_callback, name='spotify-callback'),
    path('top-artists/', views.get_top_artists, name='get_top_artists'),
    path('top-tracks/', views.get_top_tracks, name='get_top_tracks'),
    path('top-genres/', views.get_top_genres, name='get_top_genres'),
    path('new-artists/', views.get_new_artists, name='get_new_artists'),
    path('create-playlist/', views.create_most_listened_playlist, name='create_playlist'),
    path('listening-stats/', views.get_listening_stats, name='listening_stats'),
]
