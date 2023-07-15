from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class Allocations(db.Model):
    __tablename__='allocations'

    id = db.Column(db.Integer, primary_key=True)
    
    # db level
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    license_valid_to = db.Column(db.DateTime, db.ForeignKey('users.employment_end_date'))

