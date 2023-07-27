# from init import db, ma
# from marshmallow import fields
# from marshmallow.exceptions import ValidationError

# class Allocation(db.Model):
#     __tablename__= 'allocations'

#     id = db.Column(db.Integer, primary_key=True)
    
#     license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     user_valid_date = db.Column(db.DateTime, db.ForeignKey('users.employment_end_date'), default='31/12/2199')

#     # model level
#     licenses = db.relationship('Licenese', back_populates='allocation')
#     # users = db.relationship('User', back_populates='allocation')
#     end_date = db.relationship('User', back_populates='employment_end_date')

# class AllocationSchema(ma.Schema):
#     license = fields.Nested('LicenseSchema', exclude=['allocation'])

#     class Meta:
#         fields = ('id', 'license_id', 'licenses', 'users', 'end_date')


# allocation_schema = AllocationSchema()
# allocations_schema = AllocationSchema(many=True)