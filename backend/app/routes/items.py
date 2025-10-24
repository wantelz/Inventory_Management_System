from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.item import Item
from bson import ObjectId

items_bp = Blueprint('items', __name__)

def serialize_item(item):
    """Convert MongoDB item to JSON-serializable format"""
    item['_id'] = str(item['_id'])
    item['created_at'] = item.get('created_at').isoformat() if item.get('created_at') else None
    item['updated_at'] = item.get('updated_at').isoformat() if item.get('updated_at') else None
    return item

@items_bp.route('/', methods=['GET'])
@jwt_required()
def get_items():
    """Get all items with pagination and filters"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', None)
        category = request.args.get('category', None)
        
        skip = (page - 1) * limit
        items, total = Item.get_all_items(skip, limit, search, category)
        
        return jsonify({
            'items': [serialize_item(item) for item in items],
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@items_bp.route('/<item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    """Get a single item by ID"""
    try:
        item = Item.get_item_by_id(item_id)
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        return jsonify(serialize_item(item)), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@items_bp.route('/', methods=['POST'])
@jwt_required()
def create_item():
    """Create a new item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'item_code', 'category', 'quantity', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # Convert numeric fields
        data['quantity'] = int(data['quantity'])
        data['price'] = float(data['price'])
        data['min_stock'] = int(data.get('min_stock', 10))
        
        result = Item.create_item(data)
        return jsonify({
            'message': 'Item created successfully',
            'id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@items_bp.route('/<item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """Update an existing item"""
    try:
        data = request.get_json()
        
        # Convert numeric fields if present
        if 'quantity' in data:
            data['quantity'] = int(data['quantity'])
        if 'price' in data:
            data['price'] = float(data['price'])
        if 'min_stock' in data:
            data['min_stock'] = int(data['min_stock'])
        
        Item.update_item(item_id, data)
        return jsonify({'message': 'Item updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@items_bp.route('/<item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """Delete an item"""
    try:
        result = Item.delete_item(item_id)
        if result.deleted_count == 0:
            return jsonify({'message': 'Item not found'}), 404
        return jsonify({'message': 'Item deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500