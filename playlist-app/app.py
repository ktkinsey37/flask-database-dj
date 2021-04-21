from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get_or_404(playlist_id)
    print(playlist.songs, '****************************')
    return render_template("playlist.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()
    # form.songs.choices = [(s.id, f'{s.title} by {s.artist}') for s in Song.query.all()] #This is a relic of trying to render the SelectMultipleField, would be down to look at this and see if it can be made workable.
    if form.validate_on_submit():
        song_ids = request.form.getlist('song')
        new_playlist = Playlist(name=form.name.data, description=form.description.data)
        songs_to_add = Song.query.filter(Song.id.in_(song_ids)).all()
        new_playlist.songs = songs_to_add
        db.session.add(new_playlist)
        db.session.commit()
        return render_template('playlist.html', playlist=new_playlist)
    else:
        songs = Song.query.all()
        return render_template('new_playlist.html', form=form, songs=songs)


##############################################################################
# Song routes

@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get_or_404(song_id)
    return render_template('song.html', song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        return render_template('song.html', song=new_song)
    else:
        return render_template('new_song.html', form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # Loads the playlist and form
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Gets songs on playlist, then requests all songs that aren't those, makes these the choices for form
    curr_on_playlist = [s.id for s in playlist.songs]
    result = (db.session.query(Song.id, Song.title).filter(Song.id.notin_(curr_on_playlist)).all())
    choices = [(x.id, x.title) for x in result]

    form.song.choices = choices

    if form.validate_on_submit():
        # Add chosen song to playlist
        song = Song.query.get_or_404(form.song.data)
        playlist.songs.append(song)
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}", code=302)

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
