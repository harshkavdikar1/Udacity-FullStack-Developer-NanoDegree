# Capstone Project

## Content

1. [Motivation](#motivation)
2. [Start Project locally](#start-locally)
3. [API Documentation](#api)
4. [Authentification](#authentification)


<a name="motivation"></a>
## Motivations & Covered Topics

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `AWS`

<a name="start-locally"></a>
## Start Project locally

Make sure you `cd` into the correct folder (with all app files) before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server.

<ul>
<li> Initialize and activate a virtualenv: </li>

```bash
$ virtualenv --no-site-packages env_capstone
$ source env_capstone/scripts/activate
```

<li> Install the dependencies: </li>

```bash
$ pip install -r requirements.txt
```

<li> Setup Auth0 </li>
If you only want to test the API (i.e. Project Reviewer), you can
simply take the existing bearer tokens in `config.py` and `capstone.conf`.

If you already know your way around `Auth0`, just insert your data 
into `config.py` => auth0_config.

FYI: Here are the steps I followed to enable [authentification](#authentification).

<li> Run the development server: </li>

```bash 
$ python app.py
```

<li> (optional) To execute tests, run </li>

```bash 
$ python test_app.py
```
If you choose to run all tests, it should give this response if everything went fine:

```bash
$ python test_app.py
.............................
----------------------------------------------------------------------
Ran 29 tests in 15.906s

OK

```
</ul>

<a name="api"></a>
## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

**http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/**

### Authentification

Please see [API Authentification](#authentification-bearer)

### Available Endpoints

Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | PATCH  |
                    |------|-------|---------|--------|
      /actors       |  [x] |  [x]  |   [x]   |   [x]  |   
      /movies       |  [x] |  [x]  |   [x]   |   [x]  |   

### How to work with each endpoint
 
Click on a link to directly get to the ressource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.
6. Error Handling (`curl` command to trigger error + error response)

# <a name="get-actors"></a>
### 1. GET /actors

Query paginated actors.

```bash
$ curl -X GET http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors?page=1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 actors per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:actor`
- Returns: 
  1. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`
  2. **boolean** `success`

#### Example response
```js
{
    "actors": [
      {
        "id": 11,
        "name": "Polo",
        "age": 21,
        "gender": "M"
      },
      {
        "id": 12,
        "name": "Scarlett",
        "age": 27,
        "gender": "F"
      }   
    ],
    "success": true
}
```
#### Errors
If you try fetch a page which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl -X GET http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors?page=1000
```

will return

```js
{
    "error": 404,
    "message": "no actors found in database.",
    "success": false
}
```

# <a name="post-actors"></a>
### 2. POST /actors

Insert new actor into database.

```bash
$ curl -X POST http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `create:actor`
- Returns: 
  1. **integer** `Actor's details`
  2. **boolean** `success`

#### Example response
```js
{
    "Actor": {
    "age": 20,
    "gender": "M",
    "id": 1,
    "name": "John"
    },
    "success": true
}

```
#### Errors
If you try to create a new actor without a required field like `name`,
it will throw a `422` error:

```bash
$ curl -X POST http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors
```

will return

```js
{
    "success": false,
    "error": 422,
    "message": "Actor's Name is not provided."
}
```

# <a name="patch-actors"></a>
### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `edit:actor`
- Returns: 
  1. **integer** `id from updated actor`
  2. **boolean** `success`
  3. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`

#### Example response
```js
{
    "actor": {
        "id": 1,
        "name": "Marsh",
        "age": 30,
        "gender": "M"  
    },
    "success": true
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404` error:

```bash
$ curl -X PATCH http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id = 125 not found",
  "success": false
}
```

# <a name="delete-actors"></a>
### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors/5
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actor`
- Returns: 
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404` error:

```bash
$ curl -X DELETE http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/actors/125
```

will return

```js
{
    "error": 404,
    "message": "Actor with id = 125 not found.",
    "success": false
}
```

# <a name="get-movies"></a>
### 5. GET /movies

Query paginated movies.

```bash
$ curl -X GET http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies?page=1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:movie`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `name`
      - **date** `release_date`
  2. **boolean** `success`

#### Example response
```js
{
  "movies": [
    {
        "id": 1,
        "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
        "title": "Matthew first Movie",
        "rating": 5
    }
  ],
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies?page=100000
```

will return

```js
{
    "error": 404,
    "message": "No movies found in database.",
    "success": false
}
```

# <a name="post-movies"></a>
### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` (<span style="color:red">*</span>required)
       2. **date** `release_date` (<span style="color:red">*</span>optional)
       3. **date** `rating` (<span style="color:red">*</span>required)
- Requires permission: `create:movie`
- Returns: 
  1. **integer** `id from newly created movie`
  2. **boolean** `success`

#### Example response
```js
{
    "movie": {
        "id": 1,
        "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
        "title": "Test Movie 123",
        "rating": 5
    },
    "success": true
}
```
#### Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X POST http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies
```

will return

```js
{
    "error": 422,
    "message": "Movie's title is not provided.",
    "success": false
}
```

# <a name="patch-movies"></a>
### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movie`
- Returns: 
  1. **integer** `id from updated movie`
  2. **boolean** `success`
  3. List of dict of movies with following fields:
        - **integer** `id`
        - **string** `title` 
        - **date** `release_date` 

#### Example response
```js
{
    "movie": {
        "id": 1,
        "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
        "title": "Test Movie 123"
    },
    "success": true
}

```
#### Errors
If you try to update an movie with an invalid id it will throw an `404` error:

```bash
$ curl -X PATCH http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies/125
```

will return

```js
{
    "error": 404,
    "message": "Movie with id = 125 not found",
    "success": false
}
```

# <a name="delete-movies"></a>
### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movie`
- Returns: 
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404` error:

```bash
$ curl -X DELETE http://ec2-3-128-91-119.us-east-2.compute.amazonaws.com:8080/movies/125
```

will return

```js
{
    "error": 404,
    "message": "Movie with id = 125 not found",
    "success": false
}
```

# <a name="authentification"></a>
## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `Music` and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into config.py => auth0_config['AUTH0_DOMAIN'] (i.e. replace `"example-matthew.eu.auth0.com"`)
6. Click on API Tab 
7. Create a new API:
   1. Name: `Music`
   2. Identifier `Music`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into config.py => auth0_config['API_AUDIENCE'] (i.e. replace `"Example"`)

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 

# <a name="authentification-bearer"></a>
### Auth0 to use existing API
If you want to access the real, temporary API, bearer tokens for all 3 roles are included in the `config.py` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (view:actors): Can see all actors
  - GET /movies (view:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Producer (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).

For example: (Bearer token for `Executive Director`)
```js
{
    "Authorization": "Bearer your_token"
}
```