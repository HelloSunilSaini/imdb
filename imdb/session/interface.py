from datetime import timedelta
import uuid
import json
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session as DjangoSession
from django.db import close_old_connections
from flask.sessions import SessionInterface, SecureCookieSession
from imdb.utils.date_time import get_datetime_now
from imdb.utils.logger import get_root_logger

logger = get_root_logger
class MySessionInterface(SessionInterface):

    pickle_based = True
    session_class = SecureCookieSession

    def open_session(self, app, request):
        key = request.headers.get(app.auth_header_name, None)
        session = None
        try:
            session_obj = DjangoSession.objects.get(
                session_key=key,
                expire_date__gte=get_datetime_now()
            )
            dump = session_obj.session_data
            try:
                session = self.session_class(json.loads(dump))
            except:
                dump=dump.encode()
                session = self.session_class(pickle.loads(dump))
            if session.get('user_id'):
                user = User.objects.get(id=session['user_id'])
                if user.password != session.get('password_hash'):
                    session = None
                    session_obj.delete()
        except DjangoSession.DoesNotExist:
            pass

        if not session:
            session = self.session_class()
            session['key'] = key = str(uuid.uuid4())

        return session

    def save_session(self, app, session, response):
        try:
            obj = DjangoSession.objects.get(session_key=session['key'])
        except DjangoSession.DoesNotExist:
            obj = DjangoSession(session_key=session['key'])
        
        obj.session_data = json.dumps(dict(session, fix_imports=True))
        obj.expire_date =  get_datetime_now() + timedelta(days=365)
        obj.save()
        
        close_old_connections()
        

def delete_django_session(key):
    try:
        session_obj = DjangoSession.objects.get(session_key=key)
        session_obj.delete()
    except DjangoSession.DoesNotExist:
        pass

    finally:
        close_old_connections()