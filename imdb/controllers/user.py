from imdb.dao.user import get_user_by_username, get_user_by_email, \
    create_user_in_db, get_user_by_id, authorized_user
from imdb.session.interface import delete_django_session
from imdb.utils.logger import get_root_logger
from imdb.utils.custom_error import CustomError

from flask import current_app as app
from flask import session

logger = get_root_logger()

def user_exist_with_username(username):
    if get_user_by_username(username):
        return True
    else:
        return False
    

def user_exist_with_email(email):
    if get_user_by_email(email):
        return True
    else:
        return False

def create_user(user_data):
    return create_user_in_db(user_data)


def get_session_user():
    if not session.get('user_id', None):
        raise CustomError(404, "Session Not Found")
    return get_user_by_id(session['user_id'])


def validate_user(login_data):
    """
      This method is used to handle the request
      of authorizing a user.
    """
    user = authorized_user(login_data['username'], login_data['password'])
    if user:
        session['user_id'] = user.id
        session['password_hash'] = user.password
        if login_data['remember_me']:
            session.permanent = True
        logger.info("Validated the login credentials for %s", login_data['username'])
        return dict({
            'name': user.get_full_name(),
            app.auth_header_name: session.get('key')
        })
    else:
        logger.exception("Invalid username or password")
        return None


def logout_user():
    key = session.get('key')
    delete_django_session(key)
    session['user_id'] = None