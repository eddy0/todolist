from app.extensions import db
from app.models.base_model import BaseModel


class Item(db.Model, BaseModel):
    body = db.Column(db.Text)
    done = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='items')
    order = db.Column(db.Integer, autoincrement=True)
