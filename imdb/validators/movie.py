

from jsonschema import validate
from imdb.utils.logger import get_root_logger

logger = get_root_logger()

movie_post_schema = {
  "type": "object",
  "properties": {
    "99popularity": {
      "type": "number",
      "minimum" : 0,
      "maximum" : 100
    },
    "director": {
      "type": "string"
    },
    "genre": {
      "type": "array",
      "items": [
        {
          "type": "string"
        }
      ]
    },
    "imdb_score": {
      "type": "number",
      "minimum" : 0,
      "maximum" : 10
    },
    "name": {
      "type": "string"
    }
  },
  "required": [
    "99popularity",
    "director",
    "genre",
    "imdb_score",
    "name"
  ]
}


def validate_movie_post_request(request_body):
    try:
        validate(request_body, movie_post_schema)
        return True
    except Exception as e:
        logger.exception(e)
        return False
    
    
movie_put_schema = {
  "type": "object",
  "properties": {
    "id": { 
        "type": "number"
    },
    "99popularity": {
      "type": "number",
      "minimum" : 0,
      "maximum" : 100
    },
    "director": {
      "type": "string"
    },
    "genre": {
      "type": "array",
      "items": [
        {
          "type": "string"
        }
      ]
    },
    "imdb_score": {
      "type": "number",
      "minimum" : 0,
      "maximum" : 10
    },
    "name": {
      "type": "string"
    }
  },
  "required": [
    "id"
  ]
}

def validate_movie_put_request(request_body):
    try:
        validate(request_body, movie_put_schema)
        return True
    except Exception as e:
        logger.exception(e)
        return False