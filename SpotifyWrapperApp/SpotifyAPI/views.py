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
    return redirect(auth_url)

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
def get_user_top_data(access_token, type='artists', time_range='medium_term', limit=10):
    url = f"{settings.SPOTIFY_API_URL}/me/top/{type}?time_range={time_range}&limit={limit}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def user_top_artists(request):
    spotify_user = SpotifyUser.objects.get(user=request.user)
    top_artists = get_user_top_data(spotify_user.access_token, 'artists')
    return JsonResponse(top_artists)

def user_top_tracks(request):
    spotify_user = SpotifyUser.objects.get(user=request.user)
    top_tracks = get_user_top_data(spotify_user.access_token, 'tracks')
    return JsonResponse(top_tracks)