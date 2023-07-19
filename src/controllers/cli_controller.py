from flask import Blueprint
from init import db, bcrypt
from models.user import User
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created.')

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped.')

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name="Seed1 Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_position_level=True,
            is_crud_access=True,
            is_crud_admin=True,
            employment_start_date='13/01/1990'
        ),
        User(
            name="Seed2 User",
            email="userB@email.com",
            password=bcrypt.generate_password_hash('user123').decode('utf-8'),
            is_position_level=True,
            is_crud_access=True,
            is_crud_admin=False,
            employment_start_date='13/01/2001'
        ),
        User(
            name="Seed3 Admin",
            email="userC@email.com",
            password=bcrypt.generate_password_hash('user123').decode('utf-8'),
            is_position_level=True,
            is_crud_access=False,
            is_crud_admin=False,
            employment_start_date='13/01/1990'
        ),
        User(
            name="Seed4 Admin",
            email="userD@email.com",
            password=bcrypt.generate_password_hash('user123').decode('utf-8'),
            is_position_level=False,
            is_crud_access=False,
            is_crud_admin=False,
            employment_start_date='13/01/1990'
        ),
    ]
    print('Tables seeded.')

    db.session.add_all(users)

    db.session.commit()