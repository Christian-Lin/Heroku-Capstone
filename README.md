# Casting Agency Capstone

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `app.py` file to find the application. 

## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 422,
    "message": "Unable to process request. Please try again."
}
```

The API will return three error types with multiple different error messages when requests fail:

- Error 400:
    - Bad Request.
    - Permissions were not included in the JWT, auth header is missing or does not start with "Bearer".
    - Unable to process auth token.
    - Token expired or not found.

- Error 404: Resource Not Found.

- Error 422: Unable to process request (request is valid but need to check inputs and try again).

### Endpoints

#### GET '/actors'
- Fetches a paginated list of actors.
- Default arguments: 1 to 30.
- Returns: list of actors ordered by id.
```

{
  'success': True,
  'actors': [
    {
      id: 1,
      name: 'John Doe',
      age: 999,
      gender: 'male'
    }
  ]
}
```

#### GET '/movies'
- Fetches a paginated list of movies.
- Default arguments: 1 to 30.
- Returns: list of movies ordered by id.
```
{
  'success': True,
  'movies': [
    {
      id: 1,
      title: 'Fast and Furious 99',
      release_date: '2200-10-1 00:00'
    }
  ]
}
```

#### POST '/actors'
- Add a new actor.
- Arguments:
    - name: String 
    - age: Integer
    - gender: String
- Returns: An object with `success` response and the newly added actor information.
```
{
  'success': True,
  'actors': [
    {
      id: 4,
      name: 'Someone Tall',
      age: 47,
      gender: 'Male'
    }
  ]
}
```

#### POST '/movies'
- Add a new movie.
- Arguments:
    - title: String 
    - release_date: DateTime
- Returns: An object with `success` response and the newly added movie information.
```
{
  'success': True,
  'movies': [
    {
      id: 6,
      title: 'Killer Bees',
      release_date: '2025-10-1 01:25'
    }
  ]
}
```

#### Patch '/actors/<actor_id>'
- Update an actor's info.
- Arguments:
    - name: String 
    - age: Integer
    - gender: String
- Returns: An object with `success` response and the actor's updated info.
```
{
  'success': True,
  'actors': [
    {
      id: 9,
      name: 'Update Me',
      age: 22,
      gender: 'Female'
    }
  ]
}
```

#### Patch '/movies/<movie_id>'
- Update a movie's info.
- Arguments:
    - title: String 
    - release_date: DateTime
- Returns: An object with `success` response and the movie's updated info.
```
{
  'success': True,
  'movies': [
    {
      id: 1,
      title: 'Update This Movie',
      release_date: '2055-12-12 12:12'
    }
  ]
}
```

#### DELETE '/actors/<actor_id>'
- Removes an actor from the database.
- Parameters: actor id.
- Returns: An object with `success` response and the id of the deleted actor.
```
{
  'success': True,
  'id': 1
}
```

#### DELETE '/movies/<movie_id>'
- Removes a movie from the database.
- Parameters: movie id.
- Returns: An object with `success` response and the id of the deleted movie.
```
{
  'success': True,
  'id': 1
}
```

## Testing

#### Testing remote server using postman

- You can use the provided postman collection to test endpoints.
- Import the postman collection `./Casting Agency.postman_collection.json` onto Postman.
  - This collection has 3 roles that have specific permissions detailed below.
  - Roles
    - Public
      - No access
    - Casting Assistant
      - `get:actors`, `get:movies`
    - Casting Director
      - `get:actors`, `get:movies`, `post:actors`, `patch:actors`, `patch:movies`, `delete:actors`
    - Executive Producer (all permissions)
      - `get:actors`, `get:movies`, `post:actors`, `post:movies`, `patch:actors`, `patch:movies`, `delete:actors`, `delete:movies`

#### Running tests locally

(ON WINDOWS) Run the following command to create a local database with PSQL:
```bash
psql -d <db_name> -U <username> -f casting_test.psql
```

And then from the working directory:
```bash
python test_app.py
```
