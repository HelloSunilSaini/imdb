
from jsonschema import validate
from imdb.utils.logger import get_root_logger

logger = get_root_logger()

user_post_schema = {
   "type": "object",
   "properties": {
       "username": {
           "type": "string",
           "minLength": 1,
           "maxLength": 30
        },
       "password": {
            "type": "string",
            "minLength": 8
        },
       "remember_me": {
           "type": "boolean"
       }
    },
    "required": ["username", "password", "remember_me"]
}


def validate_login_request(request_body):
    try:
        validate(request_body, user_post_schema)
        return True
    except Exception as e:
        logger.exception(e)
        return False