from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
migrate.init_app(app)

from app import routes, models
