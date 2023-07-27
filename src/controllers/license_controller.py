from flask import Blueprint, request
from init import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.license import License, licenses_schema, license_schema


# Create license Blueprint
license_bp = Blueprint('license', __name__, url_prefix='/license')

### TODO Add decorator auth as admin

#Endpoint: get all licenses
@license_bp.route('/', methods=['GET'])
## TODO @jwt_required()
def get_all_apps():
    stmt = db.Select(License).order_by(License.name.desc())
    licenses = db.session.scalars(stmt)
    return licenses_schema.dump(licenses)

