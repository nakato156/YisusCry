from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from .api.api import api
from .users import user_routes
from .admin import admin_routes
from .public import public_routes
from secrets import token_urlsafe

secret = token_urlsafe(32)
app = Flask(__name__, static_folder=Config.static_folder)
app.config.from_object(Config)
app.secret_key = secret

csrf = CSRFProtect()
csrf.init_app(app)

app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(public_routes)
app.register_blueprint(api)
