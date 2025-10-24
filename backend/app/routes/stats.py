from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app import db

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/', methods=['GET'])
@jwt_required()
def get_stats():
    """Get inventory statistics"""
    try:
        items_collection = db['items']
        
        # Total items count
        total_items = items_collection.count_documents({})
        
        # Low stock items count
        low_stock = items_collection.count_documents({'quantity': {'$lte': 10}})
        
        # Total inventory value
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_value': {'$sum': {'$multiply': ['$quantity', '$price']}}
                }
            }
        ]
        result = list(items_collection.aggregate(pipeline))
        total_value = result[0]['total_value'] if result else 0
        
        # Items by category
        categories_pipeline = [
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ]
        categories = list(items_collection.aggregate(categories_pipeline))
        
        return jsonify({
            'total_items': total_items,
            'low_stock_items': low_stock,
            'total_value': round(total_value, 2),
            'categories': categories
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500