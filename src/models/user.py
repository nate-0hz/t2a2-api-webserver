from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_position_level = db.Column(db.Booolean, nullable=False, default=False)
    is_crud_access = db.Column(db.Boolean, nullable=False, default=False)
    is_crud_admin = db.Column(db.Bollean, nullable=False, default=False)
    employment_start_date = db.Column(db.DateTime, nullable=False)
    employment_end_date = db.Column(db.DateTime, nullable=True) # TODO back populate LicenseAllocation table
    
    # at db level

    # at model level    
    # move employment end date here?

class UserSchema(ma.Schema):
    allocation = fields.List(fields.Nested('AllocationSchema', exclude=['license_valid_to']))

    class Meta:
        fields = ('name', 'email', 'is_position_level', 'is_crud_access', 'is_crud_admin', 'employment_start_date', 'employment_end_date')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])


    # user_monthly_cost = calculation of monthly cost