from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.application import Application
from models.license import License
from models.allocation import Allocation
from datetime import date

db_commands = Blueprint('db', __name__)


# CLI command `flask db create`
@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created.')


# CLI command `flask db drop`
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables dropped.')


# CLI command `flask db seed`
@db_commands.cli.command('seed')
def seed_db():
    user1 = User(
        name="Admin User",
        email="admin@email.com",
        password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
        is_crud_access=True,
        is_crud_admin=True,
        employment_start_date=date(1990, 1, 13)
    )
    
    user2 = User(
        name="CRUD User",
        email="cuser@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_crud_access=True,
        is_crud_admin=False,
        employment_start_date=date(2001, 1, 13)
    )
    user3 = User(
        name="NonCRUD User1",
        email="ncuser1@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_crud_access=False,
        is_crud_admin=False,
        employment_start_date=date(2010, 6, 12),
        employment_end_date=date(2022, 10, 23)
    )
    user4 = User(
        name="NonCRUD User2",
        email="ncuser2@email.com",
        password=bcrypt.generate_password_hash('user123').decode('utf-8'),
        is_crud_access=False,
        is_crud_admin=False,
        employment_start_date=date(2021, 10, 1)
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
        application_id=application1.id,
        monthly_cost=9.95,
        total_purchased=10
    )
    license2 = License(
        name="M365-E3",
        description="Microsoft M365 E3 license",
        application_id=application1.id,
        monthly_cost=25.95,
        total_purchased=50
    )
    license3 = License(
        name="M365-E5",
        description="Microsoft M365 E5 license",
        application_id=application1.id,
        monthly_cost=34.95,
        total_purchased=15
    )
    license4 = License(
        name="Adobe-Creative-Cloud",
        description="Adobe Creative Cloud License",
        application_id=application2.id,
        monthly_cost=78.95,
        total_purchased=15
    )
    license5 = License(
        name="Sales-Force-Standard",
        description="Standard Salesforce license for Sales and Service Teams",
        application_id=application3.id,
        monthly_cost=44.95,
        total_purchased=15
    )
    
    db.session.add_all([license1, license2, license3, license4, license5])
    db.session.commit()
    print('Licenses table seeded and committed.')

    allocation1 = Allocation(
        user=user1,
        license=license3,
    )
    allocation2 = Allocation(
        user=user1,
        license=license4,
    )
    allocation3 = Allocation(
        user=user1,
        license=license5,
    )
    allocation4 = Allocation(
        user=user2,
        license=license3,
    )
    allocation5 = Allocation(
        user=user2,
        license=license4,
    )
    allocation6 = Allocation(
        user=user3,
        license=license1,
    )
    allocation7 = Allocation(
        user=user4,
        license=license1,
    )

    db.session.add_all([allocation1, allocation2, allocation3, allocation4, allocation5, allocation6, allocation7])
    db.session.commit()
    print('allocations table seeded and committed.')