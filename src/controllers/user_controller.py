from flask import Blueprint
from init import db
from flask_jwt_extended import jwt_required
from models.user import User, user_schema, users_schema
from controllers.auth_controller import authorise_as_access

# Create user blueprint
user_bp = Blueprint('user', __name__, url_prefix='/user')


# Endpoint to get all users - CRUD access restricted
@user_bp.route('/', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_all_users():
    # Queries the database and retreives all user details
    stmt = db.Select(User).order_by(User.id.desc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)


# Endpoint to get a single user - CRUD access restricted
@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_single_user(id):
    # Queries the database and retrieves the details of the user matching the user_id
    stmt = db.Select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        # Where the user exists, returns a dictionary of all users, else returns error that user not found
        return user_schema.dump(user)
    else:
        return {'error': f'User with id {id} not found.'}, 404


# Endpoint to delete a single user - CRUD access restricted
@user_bp.route('<int:id>', methods=['DELETE'])
@jwt_required()
@authorise_as_access
def delete_user(id):
    # Queries the database and retreives user details
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User \'{user.name}\' with id {id} deleted successfully.'}
    else:
        return {'error': f'User not found with id {id}.'}, 404