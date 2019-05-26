import os
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
import pika

database_uri = os.environ['PG_CONNECTION_URI']
rabbitmq_uri = os.environ['AMQP_URI']

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    RABBITMQ_URI=rabbitmq_uri
)

db = SQLAlchemy(app)

def connect_queue():
    if not hasattr(g, 'rabbitmq'):
        conn_params = pika.URLParameters(app.config['RABBITMQ_URI'])
        g.rabbitmq = pika.BlockingConnection(conn_params)
    return g.rabbitmq


def get_photo_processor_queue():
    if not hasattr(g, 'photo_processor'):
        conn = connect_queue()
        channel = conn.channel()
        channel.queue_declare(queue='photo_processor', durable=True)
        channel.queue_bind(exchange='amq.direct', queue='photo_processor')
        g.photo_processor = channel
    return g.photo_processor


@app.route("/")
def index():
    return jsonify(success=True)

@app.route("/photos/pending", methods=["GET"])
def get_pending_photos():
    from model import Photo
    photos = Photo.query.filter_by(status='pending').all()
    return jsonify(str(photos))


@app.route("/photos/process", methods=["POST"])
def process_photos():
    rdata = request.get_json()
    photo_processor = get_photo_processor_queue()
    q = get_photo_processor_queue()
    for uuid in rdata['uuid']:
        q.basic_publish(
            exchange='amq.direct',
            routing_key='photo_processor',
            body=uuid)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
