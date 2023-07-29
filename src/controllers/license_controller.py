from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.license import License, licenses_schema, license_schema
from models.application import Application
from models.allocation import Allocation
from controllers.auth_controller import authorise_as_admin, authorise_as_access


# Create license Blueprint
license_bp = Blueprint('license', __name__, url_prefix='/license')

### TODO Add decorator auth as admin

# Endpoint: get all licenses - CRUD access restricted
@license_bp.route('/', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_all_apps():
    # Queries database for a list of license types and returns a list of dictionaries of license types
    stmt = db.Select(License).order_by(License.name.desc())
    licenses = db.session.scalars(stmt)
    return licenses_schema.dump(licenses)


# Endpoint: get one license - CRUD access restricted
@license_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_single_license(id):
    # Queries database for a list of license types and returns in dictionary with license type and the application the license is associated with
    stmt = db.Select(License).filter_by(id=id)
    license = db.session.scalar(stmt)
    if license:
        return license_schema.dump(license)
    else:
        return {'error': f'License with id {id} not found.'}, 404
    

# Endpoint: delete license type - admin resticted
@license_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_one_license(id):
    # Queries the database for the specified license_id, returning the license attributes in a scalar
    stmt = db.select(License).filter_by(id=id)
    license = db.session.scalar(stmt)
    if license:
        allocations = Allocation.query.filter_by(license_id=id).all()
        if allocations:
            return {'error': f'Cannot delete license \'{license.name}\' with id {id} as it currently allcoated to at least one user.'}, 400
        else:
            # deletes the specified license and commits the change to the database
            db.session.delete(license)
            db.session.commit()
            return {'message': f'License id: {license.id} with name: {license.name} deleted successfully.'}
    else:
        return {'error': f'License not found with id {id}.'}, 404


# Endpoint: add new license type - admin restriced
@license_bp.route('/new', methods=['POST'])
@jwt_required()
@authorise_as_admin
def add_license():
    body_data = license_schema.load(request.get_json())

    # Validates if the provided application exists for the license to be assigned to it
    application_id = body_data.get('application_id')
    application = Application.query.get(application_id)
    if not application:
        # Prevents a licnese being assigned to a non-existant application
        return {'error': f'Application not found with id {application_id}'}, 404

    license = License(
        name=body_data.get('name'),
        description=body_data.get('description'),
        monthly_cost=body_data.get('monthly_cost'),
        total_purchased=body_data.get('total_purchased'),
        application_id=body_data.get('application_id'),
    )
    # adds and commits the new licenses to the database and returns the details for user confirmation
    db.session.add(license)
    db.session.commit()
    return license_schema.dump(license), 201

