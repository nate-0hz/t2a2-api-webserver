from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.application import Application, applications_schema, application_schema
from models.license import License
from controllers.auth_controller import authorise_as_admin, authorise_as_access


# Creating application Blueprint
application_bp = Blueprint('application', __name__, url_prefix='/application')


# Endpoint: get all apps - any registered user can access
@application_bp.route('/', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_all_apps():
    stmt = db.Select(Application).order_by(Application.id.desc())
    applications = db.session.scalars(stmt)
    return applications_schema.dump(applications)


# Endpoint: get single app with ID - any registered user can access
@application_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_single_app(id):
    stmt = db.Select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)
    
    if application:
        return application_schema.dump(application)
    else:
        return {'error': f'Application not found with id {id}'}, 404
    

# Endpoint: add new app - admin restricted
@application_bp.route('/new', methods=['POST'])
@jwt_required()
@authorise_as_admin
def add_app():
    body_data = application_schema.load(request.get_json())

    # Check for null non-nullable fields
    if not body_data.get('name'):
        return {'error': 'Application name is required'}, 400

    application = Application(
        name=body_data.get('name'),
        description=body_data.get('description'),
        isActive=body_data.get('isActive')
    )

    db.session.add(application)
    db.session.commit()
    return application_schema.dump(application), 201


# Endpoint: edit an app - admin restricted
@application_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@authorise_as_admin
def update_single_app(id):
    body_data = application_schema.load(request.get_json(), partial=True)
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)

    if application:
        application.name = body_data.get('name') or application.name
        application.description = body_data.get('description') or application.description
        if body_data.get('isActive') is not None:
            application.isActive = body_data.get('isActive')

        db.session.commit()
        return application_schema.dump(application)
    else:
        return {'error': f'Application not found with id {id}.'}, 404
    

# Endpoint: Delete an app - admin restricted
@application_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_admin
def delete_application(id):
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)

    if application:
        licenses = License.query.filter_by(application_id=id).all()
        # Validates is license types have been associatesd with application and if so, prevents application removal
        if licenses:
            return {'error': f'Cannot delete application \'{application.name}\' with id {id} as license types have been associated with the application. Please remove the license types first.'}
        else:
            db.session.delete(application)
            db.session.commit()
            return {'message': f'Application \'{application.name}\' with id {id} deleted successfully.'}
    else:
        return {'error': f'Application not found with id {id}.'}, 404
    
