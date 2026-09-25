import os
import sentry_sdk
import logging
import sys
from urllib.parse import urlparse

from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
from db import db
from psycopg2 import _psycopg
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

# from extensions import cache

from controllers import (
    users_blueprint,
    recipes_blueprint,
    user_socials_blueprint,
    feeds_blueprint,
    likes_blueprint,
    rates_blueprint,
    comments_blueprint,
    following_blueprint,
    collentions_blueprint,
)


# Sentry
sentry_sdk.init(
    dsn="https://affc2afb70a92276512c6b814dbaba50@o4507121964744704.ingest.de.sentry.io/4507121968480336",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


HOSTED_SUPABASE_HOST_SUFFIXES = (".supabase.com", ".supabase.co")


def hosted_database_uri():
    database_uri = os.getenv("DATABASE_URI")

    if not database_uri:
        raise RuntimeError(
            "DATABASE_URI is not set. Add the hosted Supabase connection string to .env."
        )

    host = urlparse(database_uri).hostname or ""

    if not host.endswith(HOSTED_SUPABASE_HOST_SUFFIXES):
        raise RuntimeError(
            f"DATABASE_URI must point to a hosted Supabase project, got host '{host}'. "
            "Local Supabase connections are not supported."
        )

    return database_uri


def create_app(is_test=False):
    app = Flask(__name__)
    load_dotenv()

    # Load common configuration settings from config.py
    # app.config.from_pyfile("config.py")

    # Override configuration settings as needed
    app.config.update(
        API_TITLE="HealtHub",
        API_VERSION="v1",
        OPENAPI_VERSION="3.0.2",
        OPENAPI_SWAGGER_UI_PATH="/swagger",
        OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        OPENAPI_URL_PREFIX="/",
        SQLALCHEMY_ECHO=True,
        DEBUG=True,
    )

    if is_test is True:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "TEST_DATABASE_URI", "sqlite://"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = hosted_database_uri()

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize cache with app
    # cache.init_app(app)

    # Initialize database
    db.init_app(app)
    Migrate(app, db)

    # Enable CORS
    CORS(app)

    # JWT configuration
    jwt = JWTManager(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "Tim Depok RevoU")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 36000  #  Expires in 10 hours
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 2592000  #  Expires in 30 days
    app.config["JWT_VERIFY_SUB"] = False

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(expired_token, jwt_data):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(_):
        return jsonify({"message": "Invalid token"}), 400

    @jwt.unauthorized_loader
    def unauthorized_callback(_):
        return jsonify({"message": "Unauthorized access"}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(_):
        return jsonify({"message": "Fresh token required"}), 401

    # Blueprints for controllers
    api = Api(app)
    api.register_blueprint(users_blueprint)
    api.register_blueprint(recipes_blueprint)
    api.register_blueprint(user_socials_blueprint)
    api.register_blueprint(feeds_blueprint)
    api.register_blueprint(likes_blueprint)
    api.register_blueprint(rates_blueprint)
    api.register_blueprint(comments_blueprint)
    api.register_blueprint(following_blueprint)
    api.register_blueprint(collentions_blueprint)

    # logger
    logging.basicConfig(level=logging.ERROR)

    logging.getLogger().setLevel(logging.INFO)

    app.logger.error("An unexpected error occurred")

    # Create a logger for the RecipeOriginRelationModel
    logger = logging.getLogger("recipe_origin_relation")
    logger.setLevel(logging.INFO)

    # Create a stream handler and set its level to INFO
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    # Create a formatter and set the format for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return app
