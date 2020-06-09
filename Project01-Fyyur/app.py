#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False,
                           default='https://images.unsplash.com/photo-1534294668821-28a3054f4256?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=False)
    show = db.relationship("Shows", backref="venue", lazy=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=False,
                           default='https://images.unsplash.com/photo-1534294668821-28a3054f4256?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=False)
    show = db.relationship("Shows", backref="artist", lazy=True)


class Shows(db.Model):
    __tablename__ = 'Shows'
    __table_args__ = (
        db.UniqueConstraint('artist_id', 'venue_id', 'start_time'),)

    show_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    image_link = db.Column(db.String(500), nullable=False,
                           default='https://images.unsplash.com/photo-1534294668821-28a3054f4256?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    cities = Venue.query.with_entities(
        Venue.city, Venue.state).group_by(Venue.state, Venue.city).all()

    data = []
    for city in cities:
        venues = Venue.query.filter_by(
            state=city.state).filter_by(city=city.city)

        current_city_venues = []
        for venue in venues:
            current_city_venues.append({
                'id': venue.id,
                'name': venue.name,
                'num_upcoming_shows': len([show for show in venue.show if show.start_time > datetime.now()])
            })

        data.append({
            "city": city.city,
            "state": city.state,
            "venues": current_city_venues
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    word = "%" + request.form.get("search_term", "") + "%"

    venues = Venue.query.filter(Venue.name.ilike(word))

    data = []

    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len([show for show in venue.show if show.start_time > datetime.now()])
        })

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id

    venue = Venue.query.get(venue_id)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }

    for show in venue.show:
        artist = show.artist
        if(show.start_time <= datetime.now()):
            data['past_shows'].append({
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
            })
            data['past_shows_count'] += 1
        else:
            data['upcoming_shows'].append({
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
            })
            data['upcoming_shows_count'] += 1

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    """
    Create a Venue Model and Commit the new Venue to the database.
    Throw appropriate error if there is an exception.
    """
    error = False

    try:
        venue = Venue(name=request.form["name"],
                      city=request.form["city"],
                      state=request.form["state"],
                      address=request.form["address"],
                      phone=request.form["phone"],
                      genres=request.form.getlist("genres"),
                      image_link=request.form.get("image_link"),
                      website=request.form.get("website"),
                      seeking_talent=True if request.form.get(
                          "seeking_talent") else False,
                      seeking_description=request.form.get(
                          "seeking_description"),
                      facebook_link=request.form["facebook_link"]
                      )

        # Add new venue to the Database
        db.session.add(venue)
        # Commit the changes to the database
        db.session.commit()
    except:
        # Set error flag to true
        error = True
        # Rollback the changes
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Show error mesaage to user
        if error:
            flash('An error occurred. Venue ' +
                  request.form["name"] + ' could not be listed.')
        # Show success mesaage to user
        else:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
    # Redirect to home page
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    error = False

    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue with ' +
                  venue_id + ' could not be deleted.')
    flash('Venue was deleted listed!')

    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    all_artists = Artist.query.with_entities(Artist.id, Artist.name).all()

    data = []
    for artist in all_artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

    word = "%" + request.form.get("search_term", "") + "%"

    artists = Artist.query.filter(Artist.name.ilike(word))

    data = []

    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len([show for show in artist.show if show.start_time > datetime.now()])
        })

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

    artist = Artist.query.get(artist_id)

    data = {
        "id": artist_id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": [],
        "upcoming_shows": [],
        "past_shows_count": 0,
        "upcoming_shows_count": 0,
    }

    for show in artist.show:
        venue = show.venue
        if show.start_time <= datetime.now():
            data['past_shows'].append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
            })
            data['past_shows_count'] += 1
        else:
            data['upcoming_shows'].append({
                "venue_id": venue.id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%S:%M')
            })
            data['upcoming_shows_count'] += 1

    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

    error = False

    print(artist_id)
    try:
        Artist.query.filter_by(id=artist_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artists with ' +
                  venue_id + ' could not be deleted.')
    flash('Artist was deleted listed!')

    return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.get(artist_id)

    artist = {
        "id": artist_id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": "Yes" if artist.seeking_venue == True else "No",
        "seeking_description": artist.seeking_description if artist.seeking_venue == True else "",
        "image_link": artist.image_link,
    }

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    error = False
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form["name"]
        artist.city = request.form["city"]
        artist.state = request.form["state"]
        artist.phone = request.form["phone"]
        artist.genres = request.form.getlist("genres")
        artist.website = request.form.get("website")
        artist.seeking_venue = True if request.form.get(
            "seeking_venue") else False
        artist.seeking_description = request.form.get("seeking_description")
        artist.facebook_link = request.form["facebook_link"]

        db.session.commit()
    except:
        # Set error flag to true
        error = True
        # Rollback the changes
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Show error mesaage to user
        if error:
            flash('An error occurred. Artist ' +
                  request.form["name"] + ' could not be edited.')
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.get(venue_id)

    venue = {
        "id": venue_id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": "Yes" if venue.seeking_talent == True else "No",
        "seeking_description": venue.seeking_description if venue.seeking_talent == True else "",
        "image_link": venue.image_link,
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    error = False
    try:
        venue = Venue.query.get(venue_id)

        venue.name = request.form["name"]
        venue.city = request.form["city"]
        venue.state = request.form["state"]
        venue.address = request.form["address"]
        venue.phone = request.form["phone"]
        venue.genres = request.form.getlist("genres")
        venue.website = request.form.get("website")
        venue.seeking_talent = True if request.form.get(
            "seeking_talent") else False
        venue.seeking_description = request.form.get("seeking_description")
        venue.facebook_link = request.form["facebook_link"]

        # Commit the changes to the database
        db.session.commit()
    except:
        # Set error flag to true
        error = True
        # Rollback the changes
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Show error mesaage to user
        if error:
            flash('An error occurred. Venue ' +
                  request.form["name"] + ' could not be edited.')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False

    try:
        artist = Artist(name=request.form["name"],
                        city=request.form["city"],
                        state=request.form["state"],
                        phone=request.form["phone"],
                        genres=request.form.getlist("genres"),
                        image_link=request.form.get("image_link"),
                        website=request.form.get("website"),
                        seeking_venue=True if request.form.get(
                            "seeking_venue") else False,
                        seeking_description=request.form.get(
                            "seeking_description"),
                        facebook_link=request.form["facebook_link"]
                        )
        # Add new artist to the Database
        db.session.add(artist)
        # Commit the changes to the database
        db.session.commit()
    except:
        # Set error flag to true
        error = True
        # Rollback the changes
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Show error mesaage to user
        if error:
            flash('Artist ' + request.form['name'] + ' could not be listed!')
        # Show success mesaage to user
        else:
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')
    # Redirect to home page
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

    data = []

    for show in Shows.query.all():
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.image_link,
            "start_time": str(show.start_time)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False

    try:
        show = Shows(venue_id=request.form["venue_id"],
                     artist_id=request.form["artist_id"],
                     start_time=request.form["start_time"],
                     image_link=request.form.get("image_link")
                     )
        # Add new artist to the Database
        db.session.add(show)
        # Commit the changes to the database
        db.session.commit()
    except:
        # Set error flag to true
        error = True
        # Rollback the changes
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Show error mesaage to user
        if error:
            flash('An error occurred. Show could not be listed.')
        # Show success mesaage to user
        else:
            flash('Show was successfully listed!')
    # Redirect to home page
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
