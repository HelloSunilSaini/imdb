try:
    import cPicle as pickle
except ImportError:
    import pickle
from datetime import datetime, timedelta
import uuid

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session as DjangoSession
from django.db import close_old_connections
from flask.sessions import SessionInterface, SecureCookieSession
import base64

class MySessionInterface(SessionInterface):

    pickle_based = True
    session_class = SecureCookieSession

    def open_session(self, app, request):
        key = request.headers.get(app.auth_header_name, None)
        session = None
        try:
            session_obj = DjangoSession.objects.get(
                session_key=key,
                expire_date__gte=datetime.now()
            )
            dump = str(session_obj.session_data)
            try:
                session = (self.session_class(pickle.loads(base64.b64decode(dump))))
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
        
        obj.session_data = base64.b64encode(pickle.dumps(dict(session, fix_imports=True)))
        obj.expire_date =  datetime.now() + timedelta(days=365)
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