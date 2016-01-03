from .models import Song, User


def find_matches(user):
    """
    Finds all the songs a user has in common with all users.
    :param user: the user you are finding matches for
    :return: a dictionary with key = user who has matching song's profile id and value = an array of matching songs
    """
    matches = {}
    tracks = Song.query.filter_by(user=user).all()
    for track in tracks:
        songs = Song.query.filter_by(name=track.name, artist=track.artist).all()
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
    sorted_matches = sorted(matches.items(), cmp=lambda x, y: len(x[1]) - len(y[1]), reverse=True)
    return sorted_matches


def get_recommendations(sorted_matches):
    top_match = sorted_matches[0]
    top_match_user_id = top_match[0]
    top_match_user = User.query.filter_by(profile_id=top_match_user_id).first()
    most_popular_songs = Song.query.filter_by \
        (user=top_match_user).order_by(Song.popularity.desc()).all()
    return most_popular_songs
