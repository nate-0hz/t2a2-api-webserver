from init import db, ma
from application import applications # why do I need to import this here but I don't need to import forgeign key tables for other models?
from marshmallow import fields
from marshmallow.exceptions import ValidationError


class License(db.Model):
    __tablename__= 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    license_name = db.Column(db.String(100), nullable=False)
    license_description = db.Column(db.String(150))
    is_position_level_restricted = db.Column(db.Boolean, nullable=False)
    monthly_cost = db.Column(db.Float, nullable=False)
    true_up_date = db.Column(db.DateTime)
    total_licenses_purchased = db.Column(db.Integer)

    # db level
    application_id = db.Column(db.Integer, db.ForeignKey(applications.id))