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
            actors = []

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

    @app.errorhandler(404)
    def error_404(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
