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


# Describes Many To Many relationship between actors and movies
Performance = db.Table('performances',
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True)
)

# Movies data model
class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(100), nullable=False)
    release_date = Column(db.DateTime, nullable=True)
    desc = Column(db.String(1000), nullable=True)
    rating = Column(db.Integer, nullable=False)
    actors = db.relationship("Actor", secondary=Performance, lazy='subquery',
                             backref=db.backref('performances', lazy=True))

    def __init__(self, title, rating, release_date=None, desc=None):
        self.title = title
        self.release_date = release_date
        self.desc = desc
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):

        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "desc": self.desc,
            "rating": self.rating
        }

# Actors data model
class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False)
    gender = Column(db.String(1), nullable=False)
    age = Column(db.Integer, nullable=False)
    actors = db.relationship("Movie", secondary=Performance, lazy='subquery',
                             backref=db.backref('performances', lazy=True))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):

        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }
