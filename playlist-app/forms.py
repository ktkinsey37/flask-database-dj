"""Forms for playlist app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField, PasswordField, RadioField
from wtforms.fields import SelectMultipleField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import Length, URL, Optional, NumberRange, Email, email_validator
from models import Song

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Playlist Name", validators=[Length(1,100)])
    # songs = SelectMultipleField('Songs', choices=[Song.query.all()]) # I cannot figure out how to get passing along these choices to work. It does not validate when I try to pass a tuple with the song name/artist and the song id
    description = StringField("Description of playlist", validators=[Length(1,100)])


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Song Title", validators=[Length(1,100)])
    artist = StringField("Artist", validators=[Length(1,100)])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add')
