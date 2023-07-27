from flask import Blueprint, request
from init import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.user import User, user_schema, users_schema


user_bp = Blueprint('user', __name__, url_prefix='/user')

### TODO add decorator for auth as admin ??

# Endpoint: get all users
@user_bp.route('/', methods=['GET'])
### jwt_required()
def get_all_users():
    stmt = db.Select(User).order_by(User.id.desc())
    users = db.session.scalars(stmt)
    return users_schema.dump(users)