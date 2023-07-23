from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError

class License(db.Model):
    __tablename__='licenses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    is_position_level_restricted = db.Column(db.Boolean, default=False)
    monthly_cost = db.Column(db.Numeric(precision=6, scale=2), nullable=False)
    total_purchased = db.Column(db.Integer)

    application_id = db.Column(db.Integer, db.ForeignKey('applications.id')) # TODO needs not null

    # at model level
    application = db.relationship('Application', back_populates='licenses')

class LicenseSchema(ma.Schema):
    application = fields.Nested('ApplicationSchema', exclude=['licenses'])
    
    class Meta:
        fields = ('id', 'name', 'description', 'is_position_level_restricted', 'monthly_cost', 'application', 'total_purchased')

license_schema = LicenseSchema()
licenses_schema = LicenseSchema(many=True)