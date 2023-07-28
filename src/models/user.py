from init import db, ma
from marshmallow import fields, validates
from marshmallow.exceptions import ValidationError


class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_position_level = db.Column(db.Boolean, nullable=False, default=False)
    is_crud_access = db.Column(db.Boolean, nullable=False, default=False)
    is_crud_admin = db.Column(db.Boolean, nullable=False, default=False)
    employment_start_date = db.Column(db.DateTime, nullable=False)
    employment_end_date = db.Column(db.DateTime, nullable=True) # TODO back populate LicenseAllocation table

    # at model level    
    allocation = db.relationship('Allocation', back_populates='user')

class UserSchema(ma.Schema):
    allocation = fields.List(fields.Nested('AllocationSchema', exclude=['users']))

    class Meta:
        fields = ('id', 'name', 'email', 'is_position_level', 'is_crud_access', 'is_crud_admin', 'employment_start_date', 'employment_end_date')

    @validates('email')
    def validate_email(self, email):
        if '@' not in email:
            raise ValidationError('Email address must contain the \'@\' character.')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


    # user_monthly_cost = calculation of monthly cost