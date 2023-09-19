from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
db = SQLAlchemy(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)


def register_blueprint(app):
    from src.routes.general import general_blueprint
    from src.routes.openapi import openapi
    app.register_blueprint(general_blueprint)
    app.register_blueprint(openapi)


register_blueprint(app)
