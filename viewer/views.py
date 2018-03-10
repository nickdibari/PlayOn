# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from base64 import b64encode
from collections import namedtuple

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests

from viewer.forms import PlayListForm


Song = namedtuple('Song', ['name', 'uri', 'album'])


def landing(request):
    ctx = {}

    # Display Playlist
    if request.GET.get('playlist_uri'):
        songs = []
        form = PlayListForm(request.GET)

        if form.is_valid():
            playlist_string = form.cleaned_data['playlist_uri']
            
            # Pull relevant data from URI
            # Example URI: spotify:user:<user_id>:playlist:<playlist_id>
            values = playlist_string.split(':')
            user_id = values[2]
            playlist_id = values[4]
            
            # Authenticate through Spotify API
            access_token = get_access_token()

            # Hit Spotify API for playlist
            url = '{base_url}/users/{user}/playlists/{playlist}/tracks'.format(
                base_url=settings.SPOTIFY_BASE_URL,
                user=user_id,
                playlist=playlist_id,
            )

            headers = {'Authorization': 'Bearer {}'.format(access_token)}
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()

            # Parse response for songs
            tracks = resp.json()['items']
            for track in tracks:
                track_data = track['track']
                uri = track_data['uri']
                name = track_data['name']
                album = track_data['album']['images'][0]['url']

                song = Song(name=name, uri=uri, album=album)
                songs.append(song)

            # Send to play page
            ctx['songs'] = songs
            ctx['form'] = PlayListForm()
            return render(request, 'landing.html', context=ctx)

    # Get Playlist
    else:
        ctx['form'] = PlayListForm()
        return render(request, 'landing.html', context=ctx)


def get_access_token():
    """Get access token for Spotify from client ID and secret specified in 
    configuration file. Return access token which is needed to access the
    Spotify API"""
    auth_string = '{client_id}:{client_secret}'.format(
        client_id=settings.SPOTIFY_ID,
        client_secret=settings.SPOTIFY_KEY
    )

    # Prepare request attributes
    headers = {'Authorization': 'Basic {}'.format(b64encode(auth_string))}
    post_data = {'grant_type': 'client_credentials'}

    resp = requests.post(
        'https://accounts.spotify.com/api/token',
        headers=headers,
        data=post_data
    )

    resp.raise_for_status()
    resp_data = resp.json()

    return resp_data['access_token']