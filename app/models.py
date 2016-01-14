from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(64), index=True)
    profile_id = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    songs = db.relationship('Song', backref='user', lazy='dynamic')

    def __init__(self, display_name, profile_id, email):
        if display_name is None:
            self.display_name = profile_id
        else:
            self.display_name = display_name
        self.profile_id = profile_id
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.profile_id


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    genres = db.relationship('Genre')
    songs = db.relationship('Song')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Artist %r>' % self.name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Genre %r>' % self.name


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    album = db.Column(db.String(128))
    preview_url = db.Column(db.String(128), nullable=True)
    popularity = db.Column(db.Integer, index=True)
    artist = db.relationship('Artist', uselist=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, album, artist, preview_url, popularity, user):
        self.name = name
        self.album = album
        self.artist = artist
        self.preview_url = preview_url
        self.popularity = popularity
        self.user = user

    def __repr__(self):
        return '<Song %r>' % self.name
