from os.path import dirname, abspath
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import django

django.setup()

from django.db import close_old_connections

from imdb.utils.logger import get_root_logger
from imdb.db.settings.pool import init_pool
from imdb.session.interface import MySessionInterface

from imdb.rest.ping import Ping
from imdb.rest.login import Login
from imdb.rest.logout import Logout
from imdb.rest.user import User
from imdb.rest.movie import Movie

logger = get_root_logger()
close_old_connections()
init_pool()

app = Flask("imdb")
CORS(app)

app.auth_header_name = 'Authorization'
app.session_interface = MySessionInterface()

app.root_dir = dirname(dirname(abspath(__file__)))
api = Api(app, prefix='/imdb-service/')

logger.info("Setting up Resources")

api.add_resource(Ping, 'ping/')
api.add_resource(Login, 'login/')
api.add_resource(Logout, 'logout/')
api.add_resource(User, 'user/')
api.add_resource(Movie, 'movie/', 'movie/<string:movie_id>/')

logger.info("Resource Setup Done.")

if __name__ == '__main__':
    print("app {} started..".format(app))
    app.run(host="0.0.0.0", debug=True, port=8600)
