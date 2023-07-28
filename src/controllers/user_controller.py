from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.user import User, user_schema, users_schema
from controllers.auth_controller import authorise_as_access

user_bp = Blueprint('user', __name__, url_prefix='/user')


# Endpoint to get all users - CRUD access restricted
@user_bp.route('/', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_all_users():
    stmt = db.Select(User).order_by(User.id.desc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)


# Endpoint to get a single user - CRUD access restricted
@user_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_single_user(id):
    stmt = db.Select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        return user_schema.dump(user)
    else:
        return {'error': f'User with id {id} not found.'}, 404