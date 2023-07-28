from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.allocation import Allocation, allocations_schema
from models.user import User
from models.license import License
from controllers.auth_controller import authorise_as_access

# Create allocation Blueprint
allocation_bp = Blueprint('allocation', __name__, url_prefix='/allocation')

### TODO add decorator auth as admin ??

# Endpoint: get all allocations - CRUD access restricted
@allocation_bp.route('/', methods=['GET'])
@jwt_required()
@authorise_as_access
def get_all_allocations():
    stmt = db.Select(Allocation).order_by(Allocation.id.desc())
    allocations = db.session.scalars(stmt)
    return allocations_schema.dump(allocations)


# Endpoint get allocations for specific user - CRUD access restricted
@allocation_bp.route('/user/<int:id>', methods=['GET']) ## TODO FIX: Test result where no allocation
@jwt_required()
@authorise_as_access
def get_single_user_allocation(id):
    try:
        user = User.query.get(id)
        stmt = db.Select(Allocation).filter_by(user_id=id)
        allocations = list(db.session.scalars(stmt))

        if not allocations:
            return {'error': f'No license allocations found for user with id {id}'}, 404
        else:
            allocation_dict = []
            total_monthly_cost = 0
            for allocation in allocations:
                license = allocation.license
                allocation_dict.append({
                    'license_id': allocation.license_id,
                    'license_name': license.name,
                    'monthly_cost': license.monthly_cost
                })
                total_monthly_cost =+ license.monthly_cost
            return {
                'user_id': user.id,
                'user_name': user.name,
                'licenses': allocation_dict,
                'total_monthly_cost': total_monthly_cost
            }
    except:
        return {'error': f'No user found with id {id}'}, 404

# Endpoint get allocations for specific license type - CRUD access restricted
@allocation_bp.route('/assigned_license/<int:id>', methods=['GET']) ## TODO Test: Returns result where no allocation
@jwt_required()
@authorise_as_access
def get_single_license_allocation(id):
    try:
        license = License.query.get(id)
        stmt = db.Select(Allocation).filter_by(license_id=id)
        allocations = list(db.session.scalars(stmt))

        if not allocations:
            return {'error': f'No license allocations found for licence type with id {id}'}, 404
        else:
            license_allocation_dict = []
            total_monthly_cost = 0
            for allocation in allocations:
                user = allocation.user
                license_allocation_dict.append({
                    'user_id': allocation.user_id,
                    'user_name': user.name
                    # 'monthly_cost': license.monthly_cost
                })
                # total_monthly_cost =+ license.monthly_cost
            return {
                'license_id': license.id,
                'license_name': license.name,
                'users': license_allocation_dict,
                # 'total_monthly_cost': total_monthly_cost
            }
    except:
        return {'error': f'No license found with id {id}'}, 404
