from datetime import datetime

from app.extensions import db


class BaseModel(object):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()
