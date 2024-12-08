import os

from flask import Flask


def init_app(app: Flask):
    # app.secret_key = os.getenvb(b"SECRET_KEY") or os.urandom(24)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SECRET_KEY=os.environ.get("PRINTING_HOUSE_SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("PRINTING_HOUSE_DATABASE_URI"),
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        # BASE_URL=os.getenv('BASE_URL', 'http://127.0.0.1:5000'),
    )
