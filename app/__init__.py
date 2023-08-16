from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from .api.api import api
from .users import *
from .admin import admin_routes
from .public import public_routes
from secrets import token_urlsafe
from app.context_processors.functions import utility

secret = token_urlsafe(32)
app = Flask(__name__, static_folder=Config.static_folder)
app.config.from_object(Config)
app.secret_key = secret

csrf = CSRFProtect()
csrf.exempt(public_respuesta)
csrf.exempt(public_comentario)
csrf.init_app(app)

app.context_processor(utility)
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(public_routes)
app.register_blueprint(api)
