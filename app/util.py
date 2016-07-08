from .models import Song, User, Artist, Genre
from spotify import get_artist_genres
from collections import Counter
import itertools


def find_matches(user):
    """
    Finds all the songs a user has in common with all users.
    :param user: the user you are finding matches for
    :return: a dictionary with key = user who has matching song's profile id
    and value = an array of matching songs
    """
    matches = {}
    tracks = Song.query.filter_by(user=user).all()
    for track in tracks:
        songs = Song.query.filter_by(
            name=track.name, artist=track.artist).all()
        matching_songs = [song for song in songs if song.user != user]
        for matching_song in matching_songs:
            matching_user = matching_song.user
            matching_user_id = matching_user.profile_id
            if matching_user_id in matches:
                matches[matching_user_id].append(matching_song)
            else:
                matches[matching_user_id] = [matching_song]
    return matches


def sort_matches(matches):
    """
    Sort the user matches in descending order of number of matches
    :return: a list a tuples where each tuple is modeled as
    (user_id, list of matching songs)
    """
    sorted_matches = sorted(
        matches.items(), cmp=lambda x, y: len(x[1]) - len(y[1]), reverse=True)
    return sorted_matches


def get_recommendations(sorted_matches):
    """
    get the most common genre of the most similar users matching songs
    then find most popular songs of this genre from the similar user,
    and recommend those
    """
    # put whole method in loop from 0 to len(sorted_matches)
    # continue until we have found some recommendations
    # (instead of just looking at top match)
    if len(sorted_matches) > 0:
        top_match = sorted_matches[0]
        top_match_songs = top_match[1]
        top_match_song_set = set(top_match_songs)
        # get the most common genre for top match user's songs
        genre_lists = [song.genres for song in top_match_songs]
        genres = list(itertools.chain(*genre_lists))
        genre_counts = Counter(genres)
        most_common_genre = genre_counts.most_common(1)[0][0]
        # just get the user field of a matching song instead of making db call
        top_match_user = top_match_songs[0].user
        # get all the Songs from Artists which have the most common genre
        # that also belong to the top match user
        most_common_genre_songs = Song.query.filter(Song.artist.has(
            Artist.genres.any(Genre.name == most_common_genre))).filter(
            Song.user == top_match_user).all()
        recommendations = []
        # if any songs in most_common_genre_songs are not in top matching
        # songs, add them to the recommended songs
        most_common_genre_song_set = set(most_common_genre_songs)
        recommend_set = most_common_genre_song_set - top_match_song_set
        recommendation_list = list(recommend_set)
        recommendations += recommendation_list
        if len(recommendations > 0):
            # sort by popularity, then return
            recommendations.sort(key=lambda x: x.popularity, reverse=True)
            return recommendations
    return []


def parse_track_info(spotify_tracks, user):
    """
    Spotify gives a lot of track metadata that we don't need.
    Parse out the information to build Song objects
    :param spotify_tracks: a list of user's saved tracks from Spotify API
    :return: a list of Song objects
    """
    tracks = []
    for item in spotify_tracks:
        track_info = item['track']
        album = track_info['album']['name']
        artist_name = track_info['artists'][0]['name']
        artist_id = track_info['artists'][0]['id'].encode('ascii', 'ignore')
        print artist_id
        print type(artist_id)
        # WTF? sqlalchemy thinks when doing filter_by(spotify_id=artist_id), i'm passing in an integer
        # "invalid input syntax for integer: $artist_id"
        # chanign to name for now, but would like to fix
        artist = Artist.query.filter_by(spotify_id=artist_id).first()
        if not artist:
            artist = Artist(name=artist_name, spotify_id=artist_id)
            artist.genres = get_artist_genres(artist_id)
        song_title = track_info['name']
        preview_url = track_info['preview_url']
        popularity = track_info['popularity']
        track = Song(name=song_title,
                     album=album,
                     artist=artist,
                     preview_url=preview_url,
                     popularity=popularity,
                     user=user)
        tracks.append(track)
    return tracks
