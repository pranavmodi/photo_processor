import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

database_uri = os.environ['PG_CONNECTION_URI']

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)

@app.route("/")
def index():
    return jsonify(success=True)

@app.route("/photos/pending", methods=["GET"])
def get_pending_photos():
    from model import Photo
    photos = Photo.query.all()
    return jsonify(str(photos))


@app.route("/photos/process", methods=["POST"])
def process_photos():
    from model import Photo
    photos = Photo.query.all()
    return jsonify(str(photos))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
