from init import db, ma
from marshmallow import fields



class User(db.Model):
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_crud_access = db.Column(db.Boolean, nullable=False, default=False)
    is_crud_admin = db.Column(db.Boolean, nullable=False, default=False)
    employment_start_date = db.Column(db.Date, nullable=False)
    employment_end_date = db.Column(db.Date, nullable=True) # TODO back populate LicenseAllocation table

    # at model level    
    allocation = db.relationship('Allocation', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    allocation = fields.List(fields.Nested('AllocationSchema', exclude=['users']))

    class Meta:
        fields = ('id', 'name', 'email', 'is_crud_access', 'is_crud_admin', 'employment_start_date', 'employment_end_date')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


    # user_monthly_cost = calculation of monthly cost