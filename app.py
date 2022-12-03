# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify,
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(180))
    shows = db.relationship("Show", backref="venue", lazy=True)
    website = db.Column(db.String(180))


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(180))
    shows = db.relationship("Show", backref="artist", lazy=True)
    website = db.Column(db.String(180))


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = "show"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale="en")


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []

    # query all cities and remove any duplicate by distinct
    # returns a tupple of (city, state)
    all_cities = db.session.query(Venue.city, Venue.state).distinct(
        Venue.city, Venue.state
    )

    # loop over the city tupple
    for city in all_cities:
        # search venus by thier city
        venues_by_city = (
            db.session.query(Venue.id, Venue.name)
            .filter(Venue.city == city[0])
            .filter(Venue.state == city[1])
        )

        # add the new data to the data variable
        data.append({"city": city[0], "state": city[1], "venues": venues_by_city})
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    searched_key = request.form.get("search_term")
    venues = db.session.query(Venue).filter(Venue.name.ilike(f"%{searched_key}%")).all()

    data = []
    num_upcoming_shows = 0

    for venue in venues:
        # then find corresponding show
        shows = db.session.query(Show).filter(Show.venue_id == venue.id)

        for show in shows:
            if show.start_time > datetime.now():
                num_upcoming_shows += 1

        data.append(
            {
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )

    response = {"count": len(venues), "data": data}
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    pastshows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0

    # query all venusts and filter by an id
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    shows = db.session.query(Show).filter(Show.venue_id == venue_id).all()

    data = []
    for show in shows:
        artist = (
            db.session.query(Artist.id, Artist.name, Artist.image_link)
            .filter(Artist.id == show.artist_id)
            .first()
        )

        if show.start_time > datetime.now():
            upcoming_shows_count += 1
            upcoming_shows.append(
                {
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": show.start_time.strftime("%b-%d-%y"),
                }
            )
        else:
            past_shows_count += 1
            pastshows.append(
                {
                    "artist_id": artist.id,
                    "artist_name": artist.name,
                    "artist_image_link": artist.image_link,
                    "start_time": show.start_time.strftime("%b-%d-%y"),
                }
            )
    data.append(
        {
            "id": venue.id,
            "name": venue.name,
            "genres": venue.genres.split(","),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "image_link": venue.image_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "past_shows": pastshows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(pastshows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    )

    return render_template("pages/show_venue.html", venue=list(data)[0])


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # TODO: insert form data as a new Venue record in the db, instead
    error = False
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        address = request.form.get("address")
        phone = request.form.get("phone")
        genres = ",".join(request.form.getlist("genres"))
        facebook_link = request.form.get("facebook_link")
        image_link = request.form.get("image_link")
        website_link = request.form.get("website_link")
        seeking_talent = True if request.form.get("seeking_talent") != None else False
        seeking_description = request.form.get("seeking_description")
        # TODO: modify data to be the data object returned from db insertion

        new_vene = Venue(
            name=name,
            city=city,
            state=state,
            address=address,
            phone=phone,
            genres=genres,
            facebook_link=facebook_link,
            image_link=image_link,
            website=website_link,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description,
        )

        db.session.add(new_vene)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully listed!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    error = False
    try:
        db.session.query(Show).filter(Show.venue_id == venue_id).delete()
        db.session.query(Venue).filter(Venue.id == venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if not error:
        flash(f"Venue was deleted successfully!!")
    else:
        flash(f"An error occurred. Venue could not be deleted.")

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return jsonify({"delete": "success"})


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    data = []
    artists = db.session.query(Artist).all()

    for artist in artists:
        data.append({"id": artist.id, "name": artist.name})

    data = data
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    searched_key = request.form.get("search_term", "")
    found_artists = (
        db.session.query(Artist.id, Artist.name)
        .filter(Artist.name.ilike(f"%{searched_key}%"))
        .all()
    )

    data = []
    num_upcoming_shows = 0
    for found_artist in found_artists:
        # search the shows belonging to this artist
        shows = db.session.query(Show).filter(Show.id == found_artist.id)

        # loop over shows
        for show in shows:
            if show.start_time > datetime.now():
                num_upcoming_shows += 1
        data.append(
            {
                "id": found_artist.id,
                "name": found_artist.name,
                "num_upcoming_shows": num_upcoming_shows,
            }
        )

    response = {"count": len(found_artists), "data": data}

    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    # find artist
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    shows = db.session.query(Show).filter(Show.artist_id == artist_id)

    data = []
    past_shows = []
    upcoming_shows = []
    past_shows_count = 0
    upcoming_shows_count = 0

    for show in shows:
        venue = db.session.query(Venue).filter(Venue.id == show.venue_id).first()
        if show.start_time > datetime.now():
            upcoming_shows_count += 1
            upcoming_shows.append(
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%b-%d-%y"),
                }
            )
        else:
            past_shows_count += 1
            past_shows.append(
                {
                    "venue_id": venue.id,
                    "venue_name": venue.name,
                    "venue_image_link": venue.image_link,
                    "start_time": show.start_time.strftime("%b-%d-%y"),
                }
            )
    data.append(
        {
            "id": artist.id,
            "name": artist.name,
            "genres": artist.genres.split(","),
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website_link": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }
    )

    # data = list(filter(lambda d: d["id"] == artist_id, data))[0]
    return render_template("pages/show_artist.html", artist=list(data)[0])


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    # TODO: populate form with fields from artist with ID <artist_id>

    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    artist = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
    }
    form = ArtistForm(formdata=None, data=artist)

    return render_template("forms/edit_artist.html", form=form, artist=artist)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    error = False
    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    try:
        artist.name = request.form.get("name")
        artist.genres = ",".join(request.form.getlist("genres"))
        artist.city = request.form.get("city")
        artist.state = request.form.get("state")
        artist.phone = request.form.get("phone")
        artist.website = request.form.get("website")
        artist.facebook_link = request.form.get("facebook_link")
        artist.seeking_venue = (
            True if request.form.get("seeking_venue") != None else False
        )
        artist.seeking_description = request.form.get("seeking_description")
        artist.image_link = request.form.get("image_link")
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully Updated!")
    else:

        flash(
            "An error occurred. Venue "
            + request.form["name"]
            + " could not be updated."
        )

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/artists/<artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    error = False
    try:
        artist = db.session.query(Artist).filter(Artist.id == artist_id)
        db.session.query(Show).filter(Show.artist_id == artist_id).delete()
        artist.delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        # on successful db insert, flash success
        flash("Artist was successfully Deleted!")
    else:

        flash("An error occurred. Artist  could not be deleted.")
    return jsonify({"delete": "success"})


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    # find the selected venue
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        pass
    else:
        # TODO: populate form with values from venue with ID <venue_id>
        # store genres for later splitting
        genres = venue.genres
        venue = {
            "id": venue.id,
            "name": venue.name,
            "genres": genres.split(","),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website_link": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
        }
    form = VenueForm(formdata=None, data=venue)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    error = False
    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
        venue.name = request.form.get("name")
        venue.city = request.form.get("city")
        venue.state = request.form.get("state")
        venue.address = request.form.get("address")
        venue.phone = request.form.get("phone")
        venue.genres = ",".join(request.form.getlist("genres"))
        venue.facebook_link = request.form.get("facebook_link")
        venue.image_link = request.form.get("image_link")
        venue.website_link = request.form.get("website_link")
        venue.seeking_talent = (
            True if request.form.get("seeking_talent") != None else False
        )
        venue.seeking_description = request.form.get("seeking_description")

        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        # on successful db insert, flash success
        flash("Venue " + request.form["name"] + " was successfully listed!")
    else:

        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    error = False
    try:
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")
        phone = request.form.get("phone")
        genres = ",".join(request.form.getlist("genres"))
        facebook_link = request.form.get("facebook_link")
        website_link = request.form.get("website_link")
        seeking_venue = True if request.form.get("seeking_venue") != None else False
        seeking_description = request.form.get("seeking_description")
        image_link = request.form.get("image_link")

        new_artist = Artist(
            name=name,
            city=city,
            state=state,
            phone=phone,
            genres=genres,
            facebook_link=facebook_link,
            website=website_link,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
            image_link=image_link,
        )
        # TODO: modify data to be the data object returned from db insertion
        db.session.add(new_artist)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.close()

    if not error:
        # on successful db insert, flash success
        flash("Artist " + request.form["name"] + " was successfully listed!")
    else:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be listed."
        )
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [
        {
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z",
        },
    ]

    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = []
    shows = db.session.query(Show).all()
    for show in shows:
        # find ech show's venu and artist
        venue = db.session.query(Venue).filter(Venue.id == show.venue_id).first()
        artist = db.session.query(Artist).filter(Artist.id == show.artist_id).first()
        data.append(
            {
                "venue_id": venue.id,
                "venue_name": venue.name,
                "artist_id": artist.id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": show.start_time.strftime("%d-%b-%y"),
            }
        )

    return render_template("pages/shows.html", shows=data)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    artist_id = request.form.get("artist_id")
    venue_id = request.form.get("venue_id")
    start_time = request.form.get("start_time")

    # find if the artists and venue ar exist
    find_venue = db.session.query(Venue).filter(Venue.id == venue_id)
    find_artist = db.session.query(Artist).filter(Artist.id == artist_id)

    if find_artist and artist_id:
        new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
        try:
            db.session.add(new_show)
            db.session.commit()

            # on successful db insert, flash success
            flash("Show was successfully listed!")
        except:
            db.session.rollback()
            db.session.close()
            # TODO: on unsuccessful db insert, flash an error instead.
            flash("An error occurred. Show could not be listed.")

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
