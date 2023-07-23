from flask import Blueprint, request
from init import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.application import Application, applications_schema, application_schema

# Creating application Blueprint
application_bp = Blueprint('applications', __name__, url_prefix='/application')


### TODO Add decorator to auth as admin


# Endpoint: get all apps
@application_bp.route('/', methods=['GET'])
## TODO @jwt_required()
def get_all_apps():
    stmt = db.Select(Application).order_by(Application.id.desc())
    applications = db.session.scalars(stmt)
    return applications_schema.dump(applications)


# Endpoint: add new app
@application_bp.route('/', methods=['POST'])
## TODO add @jwt_required()
def add_app():
    body_data = application_schema.load(request.get_json())

    application = Application(
        name = body_data.get('name'),
        description = body_data.get('description'),
        isActive = body_data.get('isActive')
    )

    db.session.add(application)
    db.session.commit()
    return application_schema.dump(application), 201

## TODO add GET single app with ID


# Endpoint: edit app
@application_bp.route('/<int:id>', methods=['PUT', 'PATCH']) ## TODO: FIX THIS - DOES NOT OVERWRITE
## TODO @jwt_required()
## Add admin required check
def update_single_app(id):
    body_data = application_schema.load(request.get_json(), partial=True)
    ## TODO add jwt for admin check
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)

    if application:
        application.name = body_data.get('name') or application.name
        application.description = body_data.get('description') or application.description
        application.isActive = body_data.get('isActive') or application.isActive

        db.session.commit()
        return application_schema.dump(application)
    else:
        return { 'error': f'Application not found with id {id}.'}, 404
    

@application_bp.route('/<int:id>', methods=['DELETE'])
## @jwt_required()
## TODO ADD authorise as admin
def delete_application(id):
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)
    if application:
        db.session.delete(application)
        db.session.commit()
        return { 'message': f'Application {application.id}: {application.name} deleted successfully.'}
    else:
        return { 'error': f'Application not found with id {id}.'}, 404
    
