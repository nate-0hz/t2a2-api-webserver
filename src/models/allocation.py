from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError
from datetime import datetime

class Allocation(db.Model):
    __tablename__= 'allocations'

    id = db.Column(db.Integer, primary_key=True)
    # FK
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   
    # model level
    license = db.relationship('License', back_populates='allocation', cascade='all, delete')
    user = db.relationship('User', back_populates='allocation')


class AllocationSchema(ma.Schema):
    license = fields.Nested('LicenseSchema', exclude=['allocation'])
    user_email = fields.Method('get_user_email')
    user_name = fields.Method('get_user_name')
    user_employment_end_date = fields.Method('get_employment_end_date')
    
    def get_user_email(self, obj):
        return obj.user.email
    
    def get_user_name(self,obj):
        return obj.user.name
    
    def get_employment_end_date(self, obj):
        return obj.user.employment_end_date.strftime('%Y-%m-%d') if obj.user.employment_end_date else None
    class Meta:
        fields = ('id', 'license_id', 'user_id', 'user_name', 'user_email', 'user_employment_end_date')


allocation_schema = AllocationSchema()
allocations_schema = AllocationSchema(many=True)