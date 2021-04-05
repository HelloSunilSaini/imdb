
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
       "first_name": {
           "type": "string"
        },
       "last_name": {
           "type": "string"
        },
       "email": {
           "type": "string",
           "pattern": "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,4})$",
           "minLength": 1,
           "maxLength": 50
       },
       "is_superuser": {
           "type": "boolean"
       },
       "is_staff": {
           "type": "boolean"
       },
       "is_active": {
           "type": "boolean"
       }
    },
    "required": ["username", "password", "email"]
}


def validate_user_post_request(request_body):
    try:
        validate(request_body, user_post_schema)
        return True
    except Exception as e:
        logger.exception(e)
        return False