from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class Application(db.Model):
    __tablename__='applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    isActive = db.Column(db.Boolean, default=True) # Default is true as if the application is being added, it is assumed the application is active

