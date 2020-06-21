import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Performance
from config import bearer_tokens

assistant_auth_header = {
    'Authorization': bearer_tokens['assistant']
}

director_auth_header = {
    'Authorization': bearer_tokens['director']
}

producer_auth_header = {
    'Authorization': bearer_tokens['producer']
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "capstone_test"
        # self.database_path = "postgres://{}/{}".format(
        #     'student:student@localhost:5432', self.database_name)
        self.database_path = os.environ.get("TEST_DATABASE_URL")
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
        """ Test Home Page """
        res = self.client().get('/')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'],
            "Welcome please refer to API documentation for the endpoints")

    def test_add_actor(self):
        """
        Test POST request for /actors endpoint.
        """
        actor = {
            "name": "John",
            "age": "20",
            "gender": "M"
        }

        res = self.client().post('/actors', json=actor,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        act = data["Actor"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(act["name"], "John")
        self.assertEqual(act["age"], 20)
        self.assertEqual(act["gender"], "M")
        self.assertTrue(act["id"])

    def test_422_add_actor_name(self):
        """
        Test 422 error for POST request for /actors endpoint.
        """
        actor = {
            "age": "20",
            "gender": "M"
        }

        res = self.client().post('/actors', json=actor,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's Name is not provided.")

    def test_422_add_actor_age(self):
        """
        Test 422 error for POST request for /actors endpoint.
        """
        actor = {
            "name": "John",
            "gender": "M"
        }

        res = self.client().post('/actors', json=actor,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's age is not provided.")

    def test_422_add_actor_gender(self):
        """
        Test 422 error for POST request for /actors endpoint.
        """
        actor = {
            "name": "John",
            "age": "20"
        }

        res = self.client().post('/actors', json=actor,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor's gender is not provided.")

    def test_get_actors(self):
        """
        Test GET request for /actors endpoint.
        """
        res = self.client().get('/actors', headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
        self.assertTrue(data["total_actors"])

    def test_404_get_actors(self):
        """
        Test 404 error for GET request for /actors endpoint.
        """
        res = self.client().get('/actors?page=100000',
                                headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No actors found in database.")
        self.assertEqual(data["error"], 404)

    def test_delete_actors(self):
        """
        Test DELETE request for /actors endpoint.
        """
        actor = {
            "name": "Sara",
            "age": "23",
            "gender": "F"
        }
        res = self.client().post('/actors', json=actor,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        actor = data["Actor"]

        res = self.client().delete(
            '/actors/{}'.format(actor["id"]), headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["actor_id"], actor["id"])

    def test_422_delete_actors(self):
        """
        Test 422 error for DELETE request for /actors endpoint.
        """
        res = self.client().delete('/actors/abc', headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(data["error"], 422)

    def test_404_delete_actors(self):
        """
        Test 404 error for DELETE request for /actors endpoint.
        """
        res = self.client().delete('/actors/9999999',
                                   headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor wth id = 9999999 not found.")
        self.assertEqual(data["error"], 404)

    def test_403_delete_actors(self):
        """
        Test 403 error for DELETE request for /actors endpoint.
        """
        res = self.client().delete('/actors/1', headers=assistant_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["code"], "Unauthorized")
        self.assertEqual(data["message"]["description"],
                         "Permission not found.")
        self.assertEqual(data["error"], 403)

    def test_patch_actors(self):
        """
        Test PATCH request for /actors endpoint.
        """
        actor = {
            "name": "Marsh",
            "age": 30,
            "gender": "M"
        }
        res = self.client().patch('/actors/1', json=actor,
                                  headers=producer_auth_header)
        data = json.loads(res.data)
        actor = data["actor"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(actor["name"], "Marsh")
        self.assertEqual(actor["age"], 30)
        self.assertEqual(actor["gender"], "M")

    def test_422_patch_actors(self):
        """
        Test 422 error for PATCH request for /actors endpoint.
        """
        res = self.client().patch('/actors/abc', headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(data["error"], 422)

    def test_404_patch_actors(self):
        """
        Test 404 error for PATCH request for /actors endpoint.
        """
        res = self.client().patch('/actors/999999',
                                  headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Actor wth id = 999999 not found.")
        self.assertEqual(data["error"], 404)

    def test_401_patch_actors(self):
        """
        Test 401 error for PATCH request for /actors endpoint.
        """
        res = self.client().patch('/actors/1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["code"],
                         "authorization_header_missing")
        self.assertEqual(data["message"]["description"],
                         "Authorization header is expected.")
        self.assertEqual(data["error"], 401)

    def test_get_movies(self):
        """
        Test GET request for /movies endpoint.
        """
        res = self.client().get('/movies', headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
        self.assertTrue(data["total_movies"])

    def test_401_get_actors_bearer_missing(self):
        """
        Test 401 error for GET request for /movies endpoint.
        """
        res = self.client().get('/movies', headers={"Authorization": "abc"})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["code"], "invalid_header")
        self.assertEqual(data["message"]["description"],
                         "Authorization header must be of type token bearer.")
        self.assertEqual(data["error"], 401)

    def test_404_get_movies(self):
        """
        Test 404 error for GET request for /movies endpoint.
        """
        res = self.client().get('/movies?page=100000',
                                headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "No movies found in database.")
        self.assertEqual(data["error"], 404)

    def test_add_movie(self):
        """
        Test POST request for /movies endpoint.
        """
        movie = {
            "title": "A fluke",
            "rating": 4,
            "desc": "A movie about a small boy"
        }

        res = self.client().post('/movies', json=movie,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        mov = data["movie"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(mov["title"], movie["title"])
        self.assertEqual(mov["rating"], movie["rating"])
        self.assertEqual(mov["desc"], movie["desc"])
        self.assertTrue(mov["id"])

    def test_422_add_movie_title(self):
        """
        Test 422 error for POST request for /movies endpoint.
        """
        movie = {
            "rating": 4,
            "desc": "A movie about a small boy"
        }

        res = self.client().post('/movies', json=movie,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Movie's title is not provided.")

    def test_422_add_movie_rating(self):
        """
        Test 422 error for POST request for /movies endpoint.
        """
        movie = {
            "title": "John"
        }

        res = self.client().post('/movies', json=movie,
                                 headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Movie's rating is not provided.")

    def test_patch_movies(self):
        """
        Test PATCH request for /movies endpoint.
        """
        movie = {
            "title": "A fluke",
            "rating": 4,
            "desc": "A movie about a small boy"
        }
        res = self.client().patch('/movies/1', json=movie,
                                  headers=producer_auth_header)
        data = json.loads(res.data)
        movie = data["movie"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(movie["title"], "A fluke")
        self.assertEqual(movie["rating"], 4)
        self.assertEqual(movie["desc"], "A movie about a small boy")

    def test_422_patch_movies(self):
        """
        Test 422 error for PATCH request for /movies endpoint.
        """
        res = self.client().patch('/movies/abc',
                                  headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(data["error"], 422)

    def test_404_patch_movies(self):
        """
        Test 404 error for PATCH request for /movies endpoint.
        """
        res = self.client().patch('/movies/999999',
                                  headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Movie wth id = 999999 not found.")
        self.assertEqual(data["error"], 404)

    def test_401_patch_movies(self):
        """
        Test 401 error for PATCH request for /movies endpoint.
        """
        res = self.client().patch('/movies/1')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["code"],
                         "authorization_header_missing")
        self.assertEqual(data["message"]["description"],
                         "Authorization header is expected.")
        self.assertEqual(data["error"], 401)

    def test_delete_movies(self):
        """
        Test DELETE request for /movies endpoint.
        """
        movie = {
            "title": "A fluke",
            "rating": 4,
            "desc": "A movie about a small boy"
        }
        res = self.client().post('/movies', json=movie,
                                 headers=producer_auth_header)
        data = json.loads(res.data)
        movie = data["movie"]

        res = self.client().delete(
            '/movies/{}'.format(movie["id"]), headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["movie_id"], movie["id"])

    def test_422_delete_movies(self):
        """
        Test 422 error for DELETE request for /movies endpoint.
        """
        res = self.client().delete('/movies/abc', headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")
        self.assertEqual(data["error"], 422)

    def test_404_delete_movies(self):
        """
        Test 404 error for DELETE request for /movies endpoint.
        """
        res = self.client().delete('/movies/99999',
                                   headers=producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Movie wth id = 99999 not found.")
        self.assertEqual(data["error"], 404)

    def test_403_delete_movies(self):
        """
        Test 403 error for DELETE request for /movies endpoint.
        """
        res = self.client().delete('/movies/1',
                                   headers=assistant_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["code"], "Unauthorized")
        self.assertEqual(data["message"]["description"],
                         "Permission not found.")
        self.assertEqual(data["error"], 403)


if __name__ == '__main__':
    unittest.main()
