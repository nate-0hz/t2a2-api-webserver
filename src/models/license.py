from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError

class License(db.Model):
    __tablename__='licenses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    monthly_cost = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    total_purchased = db.Column(db.Integer)
    # FK
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)

    # at model level
    application = db.relationship('Application', back_populates='licenses')
    allocation = db.relationship('Allocation', back_populates='license', cascade='all, delete')

class LicenseSchema(ma.Schema):
    application = fields.Nested('ApplicationSchema', only=['name'])
    application_id = fields.Int()
    
    class Meta:
        fields = ('id', 'name', 'description', 'monthly_cost', 'application', 'application_id', 'total_purchased')

license_schema = LicenseSchema()
licenses_schema = LicenseSchema(many=True)