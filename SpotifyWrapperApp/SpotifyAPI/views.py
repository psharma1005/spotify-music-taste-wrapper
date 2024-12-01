from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils.timezone import now
import requests
from django.conf import settings
from datetime import timedelta
from .utils import get_spotify_token
from .models import SpotifyUser

def spotify_login(request):
    scope = 'user-top-read playlist-modify-private'
    auth_url = (
        f"{settings.SPOTIFY_AUTH_URL}?"
        f"response_type=code&client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope={scope}"
    )
    return JsonResponse({'auth_url': auth_url})
    #return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    token_data = get_spotify_token(code)

    SpotifyUser.objects.update_or_create(
        user=request.user,
        defaults={
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'expires_at': now() + timedelta(seconds=token_data['expires_in']),
        },
    )
    return JsonResponse({'message': 'Spotify Authenticated Successfully'})

def get_spotify_user(request):
    try:
        spotify_user = SpotifyUser.objects.get(user=request.user)
        if spotify_user.tokens_expired():
            spotify_user.refresh_spotify_token()
        return spotify_user
    except SpotifyUser.DoesNotExist:
        return None

def get_top_artists(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/artists?limit=10', headers=headers)
    if response.status_code == 200:
        data = response.json()
        artists = [{'name': artist['name'], 'popularity': artist['popularity']} for artist in data.get('items', [])]
        return JsonResponse({'top_artists': artists})
    return JsonResponse({'error': 'Unable to fetch top artists'}, status=400)

def get_top_tracks(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=10', headers=headers)
    if response.status_code == 200:
        data = response.json()
        tracks = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in data.get('items', [])]
        return JsonResponse({'top_tracks': tracks})
    return JsonResponse({'error': 'Unable to fetch top tracks'}, status=400)

def get_top_genres(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/artists?limit=50', headers=headers)
    if response.status_code == 200:
        data = response.json()
        genre_counts = {}
        for artist in data.get('items', []):
            for genre in artist.get('genres', []):
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        return JsonResponse({'top_genres': sorted_genres[:10]})
    return JsonResponse({'error': 'Unable to fetch top genres'}, status=400)

def get_new_artists(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/artists?limit=50', headers=headers)
    if response.status_code == 200:
        data = response.json()
        current_artists = {artist['id']: artist['name'] for artist in data.get('items', [])}
        previous_artists = spotify_user.previous_top_artists or {}
        new_artists = {id: name for id, name in current_artists.items() if id not in previous_artists}
        spotify_user.previous_top_artists = current_artists
        spotify_user.save()
        return JsonResponse({'new_artists': list(new_artists.values())})
    return JsonResponse({'error': 'Unable to fetch new artists'}, status=400)

def create_most_listened_playlist(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    user_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_id = user_response.json().get('id')
    tracks_response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=20', headers=headers)
    tracks = tracks_response.json().get('items', [])
    track_uris = [track['uri'] for track in tracks]
    playlist_data = {'name': 'Most Listened Songs', 'description': 'Generated by SpotifyWrapper', 'public': False}
    playlist_response = requests.post(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers=headers,
        json=playlist_data
    )
    playlist_id = playlist_response.json().get('id')
    requests.post(
        f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
        headers=headers,
        json={'uris': track_uris}
    )
    return JsonResponse({'message': 'Playlist created successfully!'})

def get_listening_stats(request):
    spotify_user = get_spotify_user(request)
    if not spotify_user:
        return redirect('/api/login/')
    headers = {'Authorization': f'Bearer {spotify_user.access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/top/tracks?limit=50', headers=headers)
    if response.status_code == 200:
        data = response.json()
        artist_stats = {}
        for track in data.get('items', []):
            artist_name = track['artists'][0]['name']
            duration_ms = track['duration_ms']
            artist_stats[artist_name] = artist_stats.get(artist_name, 0) + duration_ms
        for artist in artist_stats:
            artist_stats[artist] = round(artist_stats[artist] / (1000 * 60 * 60), 2)
        return JsonResponse({'listening_stats': artist_stats})
    return JsonResponse({'error': 'Unable to fetch listening stats'}, status=400)
