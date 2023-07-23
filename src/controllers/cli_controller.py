from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.application import Application
from models.license import License
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
    db.session.add_all(users)
    print('Users table seeded.')

    applications = [
        Application(
            name="Microsoft M365",
            description="Microsoft M365 platform",
            isActive=True
        )
    ]
    db.session.add_all(applications)
    print('Applications table seeded.')

    licenses = [
        License(
            name="M365-F3",
            description="Microsoft M365 F3 license",
            is_position_level_restricted = False,
            application_id=1,
            monthly_cost=9.95,
            total_purchased=10
        ),
        License(
            name="M365-E3",
            description="Microsoft M365 E3 license",
            is_position_level_restricted=False,
            application_id=1,
            monthly_cost=25.95,
            total_purchased=50
        ),
        License(
            name="M365-E5",
            description="Microsoft M365 E5 license",
            is_position_level_restricted=True,
            application_id=1,
            monthly_cost=34.95,
            total_purchased=15
        )
    ]

    db.session.add_all(licenses)
    print('Licenses table seeded.')
    

    db.session.commit()
    print('Data committed to database.')