# Capstone Project


## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

### 2. POST /actors

Insert new actor into database.

```bash
$ curl -X POST https://artist-capstone-fsnd-matthew.herokuapp.com/actors
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
$ curl -X GET https://artist-capstone-fsnd-matthew.herokuapp.com/actors?page123124
```

will return

```js
{
    "success": false,
    "error": 422,
    "message": "Actor's Name is not provided."
}