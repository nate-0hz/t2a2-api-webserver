import os
from flask import Flask
from init import db, ma, bcrypt, jwt
# import controllers.auth_controller
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands
from controllers.applications_controller import application_bp
from controllers.license_controller import license_bp
# from controllers.allocation_controller import allocation_bp
from controllers.user_controller import user_bp
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY']=os.environ.get('JWT_SECRET_KEY')

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404
    

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    ## Blueprints registered here
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(application_bp)
    app.register_blueprint(license_bp)
    # app.register_blueprint(allocation_bp)
    app.register_blueprint(user_bp)

    return app