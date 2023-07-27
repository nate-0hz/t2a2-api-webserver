from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.license import License, licenses_schema, license_schema
from models.application import Application


# Create license Blueprint
license_bp = Blueprint('license', __name__, url_prefix='/license')

### TODO Add decorator auth as admin

# Endpoint: get all licenses
@license_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_apps():
    stmt = db.Select(License).order_by(License.name.desc())
    licenses = db.session.scalars(stmt)
    return licenses_schema.dump(licenses)


# Endpoint: get one license
@license_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_single_license(id):
    stmt = db.Select(License).filter_by(id=id)
    license = db.session.scalar(stmt)
    if license:
        return license_schema.dump(license)
    else:
        return {'error': f'License not found with id {id}'}, 404
    

# Endpoint: delete license
@license_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
## TODO Add authorise as admin
def delete_one_app(id):
    stmt = db.select(License).filter_by(id=id)
    license = db.session.scalar(stmt)
    if license:
        db.session.delete(license)
        db.session.commit()
        return {'message': f'License id: {license.id} with name: "{license.name}" deleted successfully.'}
    else:
        return {'error': f'License not found with id {id}.'}, 404


# Endpoint: add new license
@license_bp.route('/new', methods=['POST'])
@jwt_required()
def add_license():
    body_data = license_schema.load(request.get_json())

    # Check if the provided application exists
    application_id = body_data.get('application_id')
    application = Application.query.get(application_id)
    if not application:
        return {'error': f'Application not found with id {application_id}'}, 404

    license = License(
        name=body_data.get('name'),
        description=body_data.get('description'),
        is_position_level_restricted=body_data.get('is_position_level_restricted'),
        monthly_cost=body_data.get('monthly_cost'),
        total_purchased=body_data.get('total_purchased'),
        application=application
    )

    db.session.add(license)
    db.session.commit()

    return license_schema.dump(license), 201

