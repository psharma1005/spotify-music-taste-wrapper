from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import requests
from django.conf import settings
from datetime import timedelta
from django.db.models import JSONField

class SpotifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    previous_top_artists = JSONField(default=dict, blank=True)

    def tokens_expired(self):
        return datetime.now() >= self.expires_at

    def refresh_spotify_token(self):
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': settings.SPOTIFY_CLIENT_ID,
                'client_secret': settings.SPOTIFY_CLIENT_SECRET,
            }
        )
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.expires_at = now() + timedelta(seconds=token_data['expires_in'])
            self.save()
        else:
            raise Exception('Failed to refresh access token.')
