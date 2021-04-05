
from django.contrib.auth.models import User
from imdb.utils.logger import get_root_logger

logger = get_root_logger()

def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
        return user
    except:
        return None
    
def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return user 
    except:
        return None

def get_user_by_id(user_id):
    try :
        user = User.objects.get(id=user_id)
        return user
    except:
        None

def authorized_user(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
        else:
            return None
    except:
        return None
    
def create_user_in_db(user_data):
    try:
        user = User.objects.create(username=user_data["username"])
        
        user.set_password(user_data["password"])
            
        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
            
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
            
        if "is_superuser" in user_data:
            user.is_superuser = user_data["is_superuser"]
            
        if "email" in user_data:
            user.email = user_data["email"]
            
        if "is_staff" in user_data:
            user.is_staff = user_data["is_staff"]
        
        if "is_active" in user_data:
            user.is_active = user_data["is_active"]
            
        user.save()
        return True
    except Exception as e:
        logger.exception(e)
        return False