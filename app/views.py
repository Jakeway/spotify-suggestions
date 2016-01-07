from app import app, db, lm
from flask import render_template, request, redirect, url_for, g, session
from flask_login import login_user, current_user
from .models import User, Song
from util import find_matches, get_recommendations, sort_matches
from .spotify import (get_auth_code_url,
                      get_access_token,
                      get_user_saved_tracks,
                      get_user_profile_info,
                      parse_track_info)


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    url = get_auth_code_url()
    return render_template('index.html', auth_url=url)


@app.route('/home')
def home():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    return render_template('home.html', user=user)


@app.route('/similar_users')
def similar_users():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    matches = find_matches(user)
    sorted_matches = sort_matches(matches)
    return render_template('similar_users.html', user=user, matches=sorted_matches)


@app.route('/tracks')
def users_tracks():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    if 'matches' in session:
        print 'cache hit!'
        matches = session['matches']
    else:
        print 'cache miss :('
        matches = find_matches(user)
        session['matches'] = matches
    tracks = user.songs.all()
    return render_template('tracks.html', user=user, tracks=tracks)


@app.route('/recommendations')
def recommendations():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    matches = find_matches(user)
    sorted_matches = sort_matches(matches)
    user_recommendations = get_recommendations(sorted_matches)
    return render_template('recommendations.html', recommendations=user_recommendations)


@app.route('/spotify')
def spotify():
    code = request.args.get('code')
    token = get_access_token(code)
    user_info = get_user_profile_info(token)
    profile_id = user_info['id']
    email = user_info['email']
    name = user_info['name']
    user = User.query.filter_by(profile_id=profile_id).first()
    if user is None:
        user = User(display_name=name, email=email, profile_id=profile_id)
        db.session.add(user)
        spotify_tracks = get_user_saved_tracks(token)
        tracks = parse_track_info(spotify_tracks)
        for track in tracks:
            album = track['album']
            name = track['name']
            artist = track['artist']
            preview_url = track['preview_url']
            popularity = track['popularity']
            song = Song(
                name=name, album=album, artist=artist, preview_url=preview_url, user=user, popularity=popularity)
            db.session.add(song)
        db.session.commit()
    login_user(user)
    g.user = user
    return redirect(url_for('home'))
