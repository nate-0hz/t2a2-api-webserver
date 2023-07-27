from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.application import Application
from models.license import License
from models.allocation import Allocation
from datetime import date
import json

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
    user1 = User(
        name="Seed1 Admin",
        email="admin@email.com",
        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        is_position_level=True,
        is_crud_access=True,
        is_crud_admin=True,
        employment_start_date='13/01/1990'
    )
    
    user2 = User(
        name="Seed2 User",
        email="userB@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_position_level=True,
        is_crud_access=True,
        is_crud_admin=False,
        employment_start_date='13/01/2001',
        employment_end_date='31/12/2999'
    )
    user3 = User(
        name="Seed3 Admin",
        email="userC@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_position_level=True,
        is_crud_access=False,
        is_crud_admin=False,
        employment_start_date='13/01/1990',
        employment_end_date='31/12/2999'
    )
    user4 = User(
        name="Seed4 Admin",
        email="userD@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_position_level=False,
        is_crud_access=False,
        is_crud_admin=False,
        employment_start_date='13/01/1990',
        employment_end_date='31/12/2999'
    )

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()
    print('Users table seeded and committed.')

    application1 = Application(
        name="Microsoft M365",
        description="Microsoft M365 platform",
        isActive=True
    )
    application2 = Application(
        name="Adobe Creative Cloud",
        description="Adobe Creative Cloud platform", 
        isActive=True
    )
    application3 = Application(
        name="Salesforce", 
        description="Salesforce platform", 
        isActive=True)
    
    db.session.add_all([application1, application2, application3])
    db.session.commit()
    print('Applications table seeded and committed.')

    license1 = License(
        name="M365-F3",
        description="Microsoft M365 F3 license",
        is_position_level_restricted = False,
        application_id=application1.id,
        monthly_cost=9.95,
        total_purchased=10
    )
    license2 = License(
        name="M365-E3",
        description="Microsoft M365 E3 license",
        is_position_level_restricted=False,
        application_id=application1.id,
        monthly_cost=25.95,
        total_purchased=50
    )
    license3 = License(
        name="M365-E5",
        description="Microsoft M365 E5 license",
        is_position_level_restricted=True,
        application_id=application1.id,
        monthly_cost=34.95,
        total_purchased=15
    )

    db.session.add_all([license1, license2, license3])
    db.session.commit()
    print('Licenses table seeded and committed.')

    allocation1 = Allocation(
        license=license1,
        user=user1
    )
    allocation2 = Allocation(
        license=license1,
        user=user2
    )

    db.session.add_all([allocation1, allocation2])
    db.session.commit()
    print('allocations table seeded and committed.')