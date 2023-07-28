from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
import functools

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Function to authorise admin
# Performs this by checking if the is_crud_admin attribute in the users table is True
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_crud_admin:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Without admin credentials, you are not authorised to perform that activity.'}, 403

    return wrapper


# Function to authorise with CRUD application access
# Performs this by checking if the is_crud_access attribute in the users table is True
def authorise_as_access(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.is_crud_access:
            return fn(*args, **kwargs)
        else:
            return {'error': 'Without application credentials, you are not authorised to perform that activity.'}, 403

    return wrapper


# Endpoint to register new account - CRUD application access restricted
@auth_bp.route('/register', methods=['POST'])
@jwt_required()
@authorise_as_access
def auth_register():
    try:
        # requires "name": , "email": , "password":, "employment_start_date":, "is_position_level": (default False), "is_crud_access": (default False), "is_crud_admin": (default False),
        # optional field is employment_end date
        # default fields should not be required to register, as defaults should populate.
        body_data = request.get_json()
        # in the model, create a new User instance from the user info provided in the POST request
        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        if body_data.get('password'):
            user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')
        user.is_position_level = body_data.get('is_position_level')
        user.is_crud_access = body_data.get('is_crud_access')
        user.is_crud_admin = body_data.get('is_crud_admin')
        user.employment_start_date = body_data.get('employment_start_date')
        user.employment_end_date = body_data.get('employment_end_date')

        # adds user to the session
        db.session.add(user)
        # commits user to db
        db.session.commit()
        # API response with success code
        return user_schema.dump(user),201
    except IntegrityError as err:
        #handles error is unique field is not unique, ie email address
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'error': 'Email address already in use'}, 409
        # handles error is not nullable field is null, eg
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            db.session.rollback()
            column_name = err.orig.diag.column_name
            return { 'error': f'Unable to add user, as {column_name} is required' }, 409
        

# Endpoint to allow login. The WJT bearer token validity is set in .env 
@auth_bp.route('/login', methods=['POST'])
def auth_login():
    # takes email and password
    body_data = request.get_json()
    # find user by email address
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # check if user exists and password is correct
    if user and (user.is_crud_access == True) and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id))
        return {'email': user.email,
                'token': token, 
                'is_crud_access': user.is_crud_access, 
                'is_crud_admin': user.is_crud_admin
        }
    # if user does not have is_crud_access value as True
    elif user and (user.is_crud_access == False) and bcrypt.check_password_hash(user.password, body_data.get('password')):
        return { 'error': f'{user.email} does not have application access.'}, 403
    # username or password is incorrect
    else:
        return { 'error': 'Invalid email or password.'}, 401