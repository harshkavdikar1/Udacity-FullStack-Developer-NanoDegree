from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer


database_name = "capstone"
database_path = "postgres://{}/{}".format(
    'student:student@localhost:5432', database_name)

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


class movies(db.Model):
    __table_name__ = "movies"

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(100), nullable=False)
    release_date = Column(db.DateTime, nullable=True)
    desc = Column(db.String(1000), nullable=True)
    rating = Column(db.Integer, nullable=False)
    actors = db.relationship("actor", secondary=Performance, lazy='subquery',
                             backref=db.backref('performance', lazy=True))

    def __init__(title, release_date=None, desc=None):
        self.title = title
        self.release_date = release_date
        self.desc = desc

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.commit()

    def format(self):

        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "description": self.desc,
            "rating": self.rating
        }
