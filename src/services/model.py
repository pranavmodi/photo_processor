from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, TEXT
from web import db


class Photo(db.Model):

    __tablename__ = 'photos'
    uuid = db.Column(UUID(as_uuid=True), unique=True, primary_key=True)
    url = db.Column(TEXT())
    status = db.Column(Enum('pending', 'completed', 'processing', 'failed', "male", name="photo_status",create_type=False))
    created_at = db.Column(DateTime)

    def __init__(self, name=None, email=None):
        self.uuid = uuid
        self.url = url
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return ','.join([str(self.uuid), str(self.url), str(self.status), str(self.created_at)])
