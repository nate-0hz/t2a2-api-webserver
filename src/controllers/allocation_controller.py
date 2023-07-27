from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required
from models.allocation import Allocation, allocation_schema, allocations_schema

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
