from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, TEXT, INTEGER
from web import db


class Photo(db.Model):

    __tablename__ = 'photos'
    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    url = db.Column(TEXT())
    status = db.Column(Enum('pending', 'completed', 'processing', 'failed', "male", name="photo_status",create_type=False))
    created_at = db.Column(DateTime)

    def __init__(self, uuid, url, status, created_at):
        self.uuid = uuid
        self.url = url
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return ','.join([str(self.uuid), str(self.url), str(self.status), str(self.created_at)])


class PhotoThumbnails(db.Model):

    __tablename__ = 'photo_thumbnails'
    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    photo_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('photos.uuid'))
    width = db.Column(INTEGER)
    height = db.Column(INTEGER)
    url = db.Column(TEXT())
    created_at = db.Column(DateTime)
    
    def __init__(self, uuid, photo_uuid, url, width, height, created_at):
        self.uuid = uuid
        self.photo_uuid = photo_uuid
        self.url = url
        self.width = width
        self.height = height
        self.created_at = created_at

    def __repr__(self):
        return ','.join([str(self.uuid), str(self.url), str(self.width), str(self.height), str(self.created_at)])

