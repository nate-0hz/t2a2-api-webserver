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
    # Queries database for a list of allocated licenses and returns a list of dictionaries of allocation license ids 
    stmt = db.Select(Allocation).order_by(Allocation.id.desc())
    allocations = db.session.scalars(stmt)
    return allocations_schema.dump(allocations)


# Endpoint get allocations for specific user - CRUD access restricted
@allocation_bp.route('/user/<int:id>', methods=['GET']) ## TODO FIX: Test result where no allocation
@jwt_required()
@authorise_as_access
def get_single_user_allocation(id):
    # Where a user with matching id is found, the CRUD application returns any allocated licenses associated with that user
    try:
        user = User.query.get(id)
        stmt = db.Select(Allocation).filter_by(user_id=id)
        allocations = list(db.session.scalars(stmt))

        # Where user exists but no licenses have been allocated to the user:
        if not allocations:
            return {'error': f'No license allocations found for user with id {id}'}, 404
        # Where user exists and licenses have been alocated, enough information to identify the user is returned, along with \
        # a list of licneses and the total monthly cost incurred by that user
        else:
            allocation_list = []
            total_monthly_cost = 0
            # The for loop appends each allocated license type for the user to the allocation_list and sums the monthly cost \
            # for each license alocated
            for allocation in allocations:
                license = allocation.license
                allocation_list.append({
                    'license_id': allocation.license_id,
                    'license_name': license.name,
                    'monthly_cost': license.monthly_cost
                })
                total_monthly_cost += license.monthly_cost
            return {
                'user_id': user.id,
                'user_name': user.name,
                'licenses': allocation_list,
                'total_monthly_cost': total_monthly_cost
            }
    except:
        # Where user with specifid id is not found, the error is handled with useful information
        return {'error': f'No user found with id {id}'}, 404

# Endpoint get allocations for specific license type - CRUD access restricted
@allocation_bp.route('/license/<int:id>', methods=['GET']) ## TODO Test: Returns result where no allocation
@jwt_required()
@authorise_as_access
def get_single_license_allocation(id):
    # Where a license type has been allocated, the CRUD application returns the minumum details to identify the license type \
    # along with the users who have had a license allcoated, and the total monthly cost of license type to the business.
    try:
        license = License.query.get(id)
        stmt = db.Select(Allocation).filter_by(license_id=id)
        allocations = list(db.session.scalars(stmt))

        # Where the license exists but but no allocations have been made
        if not allocations:
            return {'error': f'No license allocations found for licence type with id {id}'}, 404
        # Where the license exists and has been allocated to at least one user, enough information to identify the license is \
        # returned, along with a list of users who have the license allocated, and the sum of the total monthly cost of that type
        else:
            license_allocation_dict = []
            total_monthly_cost = 0
            for allocation in allocations:
                user = allocation.user
                license = allocation.license
                license_allocation_dict.append({
                    'user_id': allocation.user_id,
                    'user_name': user.name,
                    'monthly_cost': license.monthly_cost
                })
                total_monthly_cost += license.monthly_cost
            return {
                'license_id': license.id,
                'license_name': license.name,
                'users': license_allocation_dict,
                'total_monthly_cost': total_monthly_cost
            }
    except:
        # Where no license is found with the id specified, the error is handled with useful information
        return {'error': f'No license found with id {id}'}, 404
