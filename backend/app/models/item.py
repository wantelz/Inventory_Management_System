from app import db
from bson import ObjectId
from datetime import datetime

items_collection = db['items']

class Item:
    @staticmethod
    def create_item(item_data):
        """Create a new item in inventory"""
        item_data['created_at'] = datetime.utcnow()
        item_data['updated_at'] = datetime.utcnow()
        return items_collection.insert_one(item_data)
    
    @staticmethod
    def get_all_items(skip=0, limit=10, search=None, category=None):
        """Get all items with pagination and filters"""
        query = {}
        
        # Search filter
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'item_code': {'$regex': search, '$options': 'i'}}
            ]
        
        # Category filter
        if category:
            query['category'] = category
        
        total = items_collection.count_documents(query)
        items = list(items_collection.find(query).skip(skip).limit(limit).sort('created_at', -1))
        
        return items, total
    
    @staticmethod
    def get_item_by_id(item_id):
        """Get a single item by ID"""
        return items_collection.find_one({'_id': ObjectId(item_id)})
    
    @staticmethod
    def update_item(item_id, update_data):
        """Update an existing item"""
        update_data['updated_at'] = datetime.utcnow()
        return items_collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )
    
    @staticmethod
    def delete_item(item_id):
        """Delete an item"""
        return items_collection.delete_one({'_id': ObjectId(item_id)})
    
    @staticmethod
    def get_low_stock_items(threshold=10):
        """Get items with quantity below threshold"""
        return list(items_collection.find({'quantity': {'$lte': threshold}}))