import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Performance


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format(
            'student:student@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_home_page(self):
        res = self.client().get('/')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'], "Welcome please refer to API documentation for the endpoints")

    def test_add_actor(self):
        actor = {
            "name": "John",
            "age": "20",
            "gender": "M"
        }

        res = self.client().post('/actor', json=actor)

        data = json.loads(res.data)

        act = data["Actor"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(act["name"], "John")
        self.assertEqual(act["age"], 20)
        self.assertEqual(act["gender"], "M")
        self.assertTrue(act["id"])

    def test_422_add_actor_name(self):
        actor = {
            "age": "20",
            "gender": "M"
        }

        res = self.client().post('/actor', json=actor)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's Name is missing")

    def test_422_add_actor_age(self):
        actor = {
            "name": "John",
            "gender": "M"
        }

        res = self.client().post('/actor', json=actor)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's age is missing")

    def test_422_add_actor_gender(self):
        actor = {
            "name": "John",
            "age": "20"
        }

        res = self.client().post('/actor', json=actor)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's gender is missing")


if __name__ == '__main__':
    unittest.main()
