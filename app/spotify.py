import requests
import base64
import urllib as urllibparse
from app import app
from models import User

REDIRECT_URI = app.config['REDIRECT_URI']
SPOTIFY_ID = app.config['SPOTIFY_ID']
SPOTIFY_SECRET = app.config['SPOTIFY_SECRET']

RESPONSE_TYPE = 'code'
SCOPES = 'user-library-read user-read-email'


def get_auth_code_url():
    """
    Generate the URL a user needs to visit to give app authorization
    to access their info.
    """
    code_payload = {
        'client_id': SPOTIFY_ID,
        'response_type': RESPONSE_TYPE,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
    }

    auth_endpoint = 'https://accounts.spotify.com/authorize'
    url_params = urllibparse.urlencode(code_payload)
    return "%s?%s" % (auth_endpoint, url_params)


def get_access_token(code):
    """
    Calls Spotify's token endpoint to retrieve an access token used to make
    authorized API calls to Spotify.
    :param code: the authorization code given by Spotify to exchange for the
    access token.
    :return: the access token
    """
    token_endpoint = 'https://accounts.spotify.com/api/token'

    token_payload = {
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    auth_header = base64.b64encode(SPOTIFY_ID + ':' + SPOTIFY_SECRET)
    headers = {'Authorization': 'Basic %s' % auth_header}
    r = requests.post(token_endpoint, data=token_payload, headers=headers)
    token_json = r.json()
    token = token_json['access_token']
    return token


def get_user_profile_info(token):
    """
    Calls the get current user's profile endpoint on Spotify.
    :param token: access token attained from Spotify on behalf of user
    :return: a User object
    """
    user_profile_endpoint = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': 'Bearer %s' % token}

    r = requests.get(user_profile_endpoint, headers=headers)
    profile = r.json()

    display_name = profile['display_name']
    profile_id = profile['id']
    email = profile['email']

    return User(display_name=display_name,
                profile_id=profile_id,
                email=email)


def get_user_saved_tracks(token):
    """
    Fetch all the tracks a user has saved to their library.
    :param token: access token attained from Spotify on behalf of user
    :return: a list of user's saved tracks and corresponding track metadata
    """
    saved_tracks_endpoint = 'https://api.spotify.com/v1/me/tracks'
    saved_tracks = []
    headers = {'Authorization': 'Bearer %s' % token}

    # handles initial call to tracks endpoint
    r = requests.get(saved_tracks_endpoint, headers=headers)
    track_json = r.json()
    saved_tracks += track_json['items']

    next_page = track_json['next']
    # saved tracks endpoint is paginated
    while next_page:
        r = requests.get(next_page, headers=headers)
        track_json = r.json()
        saved_tracks += track_json['items']
        next_page = track_json['next']

    return saved_tracks
