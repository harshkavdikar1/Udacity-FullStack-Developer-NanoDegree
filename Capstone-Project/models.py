from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer


database_name = "capstone"
database_path = "postgres://{}/{}".format('student:student@localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    Setup db configurations
    Initialize database to app
    Create the tables according to models if they don't exist already.
    """

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()