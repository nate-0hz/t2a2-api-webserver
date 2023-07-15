from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    is_position_level = db.Column(db.Booolean, nullable=False)
    employment_start_date = db.Column(db.DateTime, nullable=False)
    employment_end_date = db.Column(db.DateTime, nullable=True)
    
    
    # at model level    
    # user_monthly_cost = calculation of monthly cost