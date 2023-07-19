from init import db, ma
from marshmallow import fields
from marshmallow.exceptions import ValidationError

class Application(db.Model):
    __tablename__='applications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    isActive = db.Column(db.Boolean, default=True)


class ApplicationSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'name', 'description', 'isActive')

application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)

