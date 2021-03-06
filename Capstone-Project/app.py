import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
from flask_migrate import Migrate
from auth import requires_auth, AuthError


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)

    ROWS_PER_PAGE = 10

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "success": True,
            "message": "Welcome please refer to API" +
            " documentation for the endpoints"
        })

    @app.route("/actors", methods=["GET"])
    @requires_auth('read:actor')
    def get_actors(token):
        """
        Returns paginated actors object
        Tested by:
            Success:
                - test_get_actors
            Error:
                - test_404_get_actors
        """

        page = int(request.args.get("page", 1))

        start = (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        actors = Actor.query.all()

        actors = [actor.format() for actor in actors]

        if len(actors) < start or start < 0:
            return jsonify({
                "error": 404,
                "message": "No actors found in database.",
                "success": False
            }), 404

        return jsonify({
            "actors": actors[start:end],
            "success": True,
            "total_actors": len(actors)
        })

    @app.route("/actors", methods=["POST"])
    @requires_auth('create:actor')
    def add_actor(token):
        """
        Inserts a new Actor
        Tested by:
            Success:
                - test_add_actor
            Error:
                - test_422_add_actor_name
                - test_422_add_actor_age
                - test_422_add_actor_gender
        """

        data = request.get_json()

        if not data.get("name"):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Actor's Name is not provided."
            }), 422

        if not data.get("age"):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Actor's age is not provided."
            }), 422

        if not data.get("gender"):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Actor's gender is not provided."
            }), 422

        try:
            actor = Actor(name=data["name"],
                          age=data["age"], gender=data["gender"])
            actor.insert()
        except Exception:
            abort(500)

        return jsonify({
            "success": True,
            "Actor": actor.format()
        })

    @app.route("/actors/<actor_id>", methods=["PATCH"])
    @requires_auth("edit:actor")
    def update_actor(token, actor_id):
        """
        Edit an existing Actor
        Tested by:
            Success:
                - test_patch_actors
            Error:
                - test_422_patch_actors
                - test_404_patch_actors
                - test_401_patch_actors
        """
        try:
            actor_id = int(actor_id)
            actor = Actor.query.get(actor_id)
        except Exception:
            abort(422)

        if not actor:
            return jsonify({
                "error": 404,
                "message": "Actor wth id = {} not found.".format(actor_id),
                "success": False
            }), 404

        data = request.get_json()

        actor.name = data.get('name', actor.name)
        actor.age = data.get('age', actor.age)
        actor.gender = data.get('gender', actor.gender)

        try:
            actor.update()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route("/actors/<actor_id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor(token, actor_id):
        """
        Delete an existing Actor
        Tested by:
            Success:
                - test_delete_actors
            Error:
                - test_404_delete_actors
                - test_403_delete_actors
                - test_422_delete_actors
        """

        try:
            actor_id = int(actor_id)
            actor = Actor.query.get(actor_id)
        except Exception:
            abort(422)

        if not actor:
            return jsonify({
                "error": 404,
                "message": "Actor wth id = {} not found.".format(actor_id),
                "success": False
            }), 404

        try:
            actor.delete()
        except Exception:
            abort(500)

        return jsonify({
            "actor_id": actor_id,
            "success": True
        })

    @app.route("/movies", methods=["GET"])
    @requires_auth('read:movie')
    def get_movies(token):
        """
        Returns paginated movies object
        Tested by:
            Success:
                - test_get_movies
            Error:
                - test_401_get_actors_bearer_missing
                - test_404_get_movies
        """

        page = int(request.args.get("page", 1))

        start = (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE

        movies = Movie.query.all()

        movies = [movie.format() for movie in movies]

        if len(movies) < start or start < 0:
            return jsonify({
                "error": 404,
                "message": "No movies found in database.",
                "success": False
            }), 404

        return jsonify({
            "movies": movies[start:end],
            "success": True,
            "total_movies": len(movies)
        })

    @app.route("/movies", methods=["POST"])
    @requires_auth('create:movie')
    def add_movie(token):
        """
        Inserts a new movie
        Tested by:
            Success:
                - test_add_movie
            Error:
                - test_422_add_movie_title
                - test_422_add_movie_rating
        """

        data = request.get_json()

        if not data.get("title"):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Movie's title is not provided."
            }), 422

        if not data.get("rating"):
            return jsonify({
                "success": False,
                "error": 422,
                "message": "Movie's rating is not provided."
            }), 422

        try:
            movie = Movie(
                title=data["title"],
                rating=data["rating"],
                release_date=data.get("release_date"),
                desc=data.get("desc"))
            movie.insert()
        except Exception:
            abort(500)

        return jsonify({
            "success": True,
            "movie": movie.format()
        })

    @app.route("/movies/<movie_id>", methods=["PATCH"])
    @requires_auth('edit:movie')
    def update_movie(token, movie_id):
        """
        Edit an existing Movie
        Tested by:
            Success:
                - test_patch_movies
            Error:
                - test_422_patch_movies
                - test_404_patch_movies
                - test_401_patch_movies
        """
        try:
            movie_id = int(movie_id)
            movie = Movie.query.get(movie_id)
        except Exception:
            abort(422)

        if not movie:
            return jsonify({
                "error": 404,
                "message": "Movie wth id = {} not found.".format(movie_id),
                "success": False
            }), 404

        data = request.get_json()

        movie.title = data.get('title', movie.title)
        movie.rating = data.get('rating', movie.rating)
        movie.desc = data.get('desc', movie.desc)
        movie.release_date = data.get('release_date', movie.release_date)

        try:
            movie.update()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route("/movies/<movie_id>", methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        """
        Delete an existing Movie
        Tested by:
            Success:
                - test_delete_movies
            Error:
                - test_403_delete_movies
                - test_404_delete_movies
                - test_422_delete_movies
        """

        try:
            movie_id = int(movie_id)
            movie = Movie.query.get(movie_id)
        except Exception:
            abort(422)

        if not movie:
            return jsonify({
                "error": 404,
                "message": "Movie wth id = {} not found.".format(movie_id),
                "success": False
            }), 404

        try:
            movie.delete()
        except Exception:
            abort(500)

        return jsonify({
            "movie_id": movie_id,
            "success": True
        })

    @app.errorhandler(404)
    def resource_not_found(error):
        """
        Error Handler for 404
        """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """
        Error Handler for 422
        """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        """
        Error Handler for 500
        """
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong!!"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        """
        Error Handler for 400
        """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Error Handler for Authorization Error
        """
        return jsonify({
            "success": False,
            "error": ex.status_code,
            'message': ex.error
        }), ex.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
