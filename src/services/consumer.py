import os
import sys
import functools
import pika
import json
import urllib.request
from PIL import Image, ImageOps
import datetime
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = create_engine(os.environ['PG_CONNECTION_URI'])
    Session = sessionmaker(bind=engine)
    return Session


def process_message(chan, method_frame, _header_frame, body, userdata=None):
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)

    process_photo(body.decode("utf-8"))


def process_photo(photo_uuid):
    ## mark the db status as processing
    from model import Photo
    Session = create_session()
    session = Session()
    photo = session.query(Photo).filter_by(uuid=photo_uuid).first()

    if photo is None:
        return

    if photo.status == 'pending':
        try:
            photo.status = 'processing'
            session.flush()
            height, width, path = generate_thumbnail(photo)
            photo.status = 'completed'

            ## Add to photo thumbnails
            from model import PhotoThumbnails
            created_at = datetime.datetime.now()
            tn_uuid = uuid.uuid1()
            pt = PhotoThumbnails(tn_uuid, photo.uuid, path, width, height, created_at)
            session.add(pt)

        except Exception as e:
            photo.status = 'failed'

    elif photo.status == 'processing':
        return

    session.commit()
    return


def generate_thumbnail(photo):
    ## Download image
    response = urllib.request.urlretrieve(photo.url)
    image = Image.open(response[0])
    image.thumbnail((320, 320))
    im_path = '/waldo-app-thumbs/' +str(photo.uuid) + '.thumbnail'
    image.save(im_path, "JPEG")
    return image.height, image.width, im_path


def main():
    conn_params = pika.URLParameters(os.environ['AMQP_URI'])
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue='photo_processor', durable=True, auto_delete=False)

    on_message_callback = functools.partial(
        process_message, userdata='on_message_userdata')
    
    channel.basic_consume('photo_processor', on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == '__main__':
    main()
