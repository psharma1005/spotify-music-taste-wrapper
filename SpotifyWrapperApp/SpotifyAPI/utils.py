import requests
from django.conf import settings

def get_spotify_token(code):
    """Exchange code for access and refresh tokens."""
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(settings.SPOTIFY_TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()