import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
from flask_migrate import Migrate


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
            "message": "Welcome please refer to API documentation for the endpoints"
        })

    @app.route("/actor", methods=["GET"])
    def get_actors():

        page = int(request.args.get("page", 1))

        start = (page - 1)*ROWS_PER_PAGE
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

    @app.route("/actor", methods=["POST"])
    def add_actor():

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

    @app.route("/actor/<actor_id>", methods=["PATCH"])
    def update_actor(actor_id):

        try:
            actor_id = int(actor_id)
            actor = Actor.query.get(actor_id)
        except:
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
        except:
            abort(500)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route("/actor/<actor_id>", methods=["DELETE"])
    def delete_actor(actor_id):

        try:
            actor_id = int(actor_id)
            actor = Actor.query.get(actor_id)
        except:
            abort(422)

        if not actor:
            return jsonify({
                "error": 404,
                "message": "Actor wth id = {} not found.".format(actor_id),
                "success": False
            }), 404

        try:
            actor.delete()
        except:
            abort(500)

        return jsonify({
            "actor_id": actor_id,
            "success": True
        })

    @app.route("/movie", methods=["GET"])
    def get_movies():

        page = int(request.args.get("page", 1))

        start = (page - 1)*ROWS_PER_PAGE
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

    @app.route("/movie", methods=["POST"])
    def add_movie():

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
            movie = Movie(title=data["title"], rating=data["rating"], release_date=data.get(
                "release_date"), desc=data.get("desc"))
            movie.insert()
        except Exception:
            abort(500)

        return jsonify({
            "success": True,
            "movie": movie.format()
        })

    @app.route("/movie/<movie_id>", methods=["PATCH"])
    def update_movie(movie_id):

        try:
            movie_id = int(movie_id)
            movie = Movie.query.get(movie_id)
        except:
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
        except:
            abort(500)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route("/movie/<movie_id>", methods=["DELETE"])
    def delete_movie(movie_id):

        try:
            movie_id = int(movie_id)
            movie = Movie.query.get(movie_id)
        except:
            abort(422)

        if not movie:
            return jsonify({
                "error": 404,
                "message": "Movie wth id = {} not found.".format(movie_id),
                "success": False
            }), 404

        try:
            movie.delete()
        except:
            abort(500)

        return jsonify({
            "movie_id": movie_id,
            "success": True
        })

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong!!"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400


    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            'message': ex.error
        }), 401

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
