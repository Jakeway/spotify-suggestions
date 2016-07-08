import traceback
import logging
from app import app, db, lm
from flask import render_template, request, redirect, url_for, g, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from .util import (find_matches,
                   sort_matches,
                   get_recommendations,
                   parse_track_info)
from .spotify import (get_auth_code_url,
                      get_access_token,
                      get_user_profile_info,
                      get_user_saved_tracks)


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


@login_required
@app.route('/home')
def home():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    return render_template('home.html', user=user)


@login_required
@app.route('/similar_users')
def similar_users():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    if 'sorted_matches' not in session:
        if 'matches' in session:
            matches = session['matches']
        else:
            matches = find_matches(user)
            session['matches'] = matches
        sorted_matches = sort_matches(matches)
        session['sorted_matches'] = sorted_matches
    else:
        print 'cache hit'
        sorted_matches = session['sorted_matches']
    return render_template('similar_users.html',
                           user=user,
                           matches=sorted_matches)


@login_required
@app.route('/tracks')
def users_tracks():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    tracks = user.songs.all()
    return render_template('tracks.html', user=user, tracks=tracks)


@login_required
@app.route('/recommendations')
def recommendations():
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('index'))
    user = g.user
    if 'sorted_matches' not in session:
        matches = []
        if 'matches' in session:
            matches = session['matches']
        else:
            matches = find_matches(user)
            session['matches'] = matches
        sorted_matches = sort_matches(matches)
        session['sorted_matches'] = sorted_matches
    else:
        print 'cache hit'
        sorted_matches = session['sorted_matches']
    user_recommendations = get_recommendations(sorted_matches)
    return render_template('recommendations.html',
                           recommendations=user_recommendations)


@app.route('/spotify')
def spotify():
    code = request.args.get('code')
    print 'in spotify(): able to get code from spotify'
    token = get_access_token(code)
    print 'in spotify(): able to get token from spotify'
    spotify_user = get_user_profile_info(token)
    print 'in spotify(): able to get spotify_user'
    try:
        user = User.query.filter_by(profile_id=spotify_user.profile_id).first()
    except Exception as e:
        logging.error(traceback.format_exc())

    print 'query User table for spotify_user'
    # user is None -> first time using spotify service
    if user is None:
        print 'user is none'
        spotify_user.authenticated = True
        db.session.add(spotify_user)
        spotify_tracks = get_user_saved_tracks(token)
        tracks = parse_track_info(spotify_tracks, spotify_user)
        for track in tracks:
            db.session.add(track)
        db.session.commit()
        login_user(spotify_user)
        g.user = spotify_user
    else:
        print user
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        g.user = user
    return redirect(url_for('home'))


@login_required
@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))
