import os
from flask import Flask
from init import db, ma, bcrypt, jwt

from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
    app.confirg['JWT_SECRET_KEY']=os.environ.get('JWT_SECRET_KEY')

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

    ## Todo: Register blueprints here

    return app