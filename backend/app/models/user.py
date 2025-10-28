from app import db
import bcrypt

users_collection = db['users']

class User:
    @staticmethod
    def create_user(username, email, password):
        #Create a new user with hashed password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': 'user'
        }
        return users_collection.insert_one(user)
    
    @staticmethod
    def find_by_email(email):
        #Find a user by email
        return users_collection.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        #Find a user by ID
        from bson import ObjectId
        return users_collection.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        #Verify if provided password matches stored hash
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)