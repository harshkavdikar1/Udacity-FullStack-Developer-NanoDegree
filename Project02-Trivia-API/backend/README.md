# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample Response:
```

```

GET '/questions?page=<page_number>'
- Fetches a paginated dictionary of questions of all available categories
- Request Arguments (optional): page:int
- Sample Response:

```

```

DELETE /questions/<question_id> 
- Delete an existing questions from the repository of available questions.
- Request Arguments: question_id:int
- Sample Response:

```

```

POST /questions 
- Add a new question to the repository of available questions.
- Request Arguments: None
- Request body: {question:string, answer:string, difficulty:int, category:string}
- Sample response:

```

```

POST /search 
- Fetches all questions where a substring matches the search term (not case-sensitive)
- Request Arguments: None
- Request body: {searchTerm:string}
- Sample response:

```

```


GET /categories/<int:category_id>/questions 
- Fetches a dictionary of questions for the specified category
- Request Argument: category_id:int
- Sample response:

```

```

POST /quizzes 
- Fetches one random question within a specified category. Previously asked questions are not asked again.
- Request Argument: None
- Request body: {previous_questions: arr, quiz_category: {id:int, type:string}}
- Sapmle response:

```

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```