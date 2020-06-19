# Capstone Project


## API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

**Base URL**

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
$ curl -X GET /actors?page=1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 actors per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:actors`
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
$ curl -X GET /actors?page=1000
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
$ curl -X POST /actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `create:actors`
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
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET /actors
```

will return

```js
{
    "success": false,
    "error": 422,
    "message": "Actor's Name is not provided."
}
```

### 3. PATCH /actors

Edit an existing Actor

```bash
$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `edit:actors`
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
$ curl -X PATCH /actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id = 125 not found",
  "success": false
}
```

### 4. DELETE /actors

Delete an existing Actor

```bash
$ curl -X DELETE /actors/5
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
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
$ curl -X DELETE /actors/125
```

will return

```js
{
    "error": 404,
    "message": "Actor with id = 125 not found.",
    "success": false
}
```

### 5. GET /movies

Query paginated movies.

```bash
$ curl -X GET /movies?page1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:movies`
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
        "title": "Matthew first Movie"
    }
  ],
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/movies?page123124
```

will return

```js
{
    "error": 404,
    "message": "No movies found in database.",
    "success": false
}
```

### 6. POST /movies

Insert new Movie into database.

```bash
$ curl -X POST /movie
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` (<span style="color:red">*</span>required)
       2. **date** `release_date` (<span style="color:red">*</span>required)
- Requires permission: `create:movies`
- Returns: 
  1. **integer** `id from newly created movie`
  2. **boolean** `success`

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
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET /movie?page123124
```

will return

```js
{
    "error": 422,
    "message": "Movie's title is not provided.",
    "success": false
}
```

### 7. PATCH /movies

Edit an existing Movie

```bash
$ curl -X PATCH /movie/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movies`
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
$ curl -X PATCH /movie/125
```

will return

```js
{
    "error": 404,
    "message": "Movie with id = 125 not found",
    "success": false
}
```

### 8. DELETE /movies

Delete an existing movie

```bash
$ curl -X DELETE movie/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`
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
$ curl -X DELETE /movie/125
```

will return

```js
{
    "error": 404,
    "message": "Movie with id = 125 not found",
    "success": false
}
```