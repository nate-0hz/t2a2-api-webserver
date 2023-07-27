from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.allocation import Allocation, allocations_schema
from models.user import User

# Create allocation Blueprint
allocation_bp = Blueprint('allocation', __name__, url_prefix='/allocation')

### TODO add decorator auth as admin ??

# Endpoint: get all allocations
@allocation_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_allocations():
    stmt = db.Select(Allocation).order_by(Allocation.id.desc())
    allocations = db.session.scalars(stmt)
    return allocations_schema.dump(allocations)


# Endpoint get allocations for specific user
@allocation_bp.route('/<int:id>', methods=['GET']) ## TODO FIX: Returns result where no allocation
@jwt_required()
def get_single_user_allocation(id):
    try:
        user = User.query.get(id)
        stmt = db.Select(Allocation).filter_by(user_id=id)
        allocation = db.session.scalars(stmt)
        if not allocation:
            return {'error': f'No license allocations found for user with id {id}'}, 404
        else:
            allocation_dict = [{'license_id': allocation.license_id, 
                                'license_name': allocation.license.name, 
                                'monthly_cost': allocation.license.monthly_cost} for allocation in allocation]
            return {
                'user_id': user.id,
                'user_name': user.name,
                'licenses': allocation_dict}
    except:
        return {'error': f'No user found with id {id}'}, 404


