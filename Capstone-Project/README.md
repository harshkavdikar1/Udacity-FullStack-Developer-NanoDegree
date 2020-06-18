# Capstone Project


## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

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