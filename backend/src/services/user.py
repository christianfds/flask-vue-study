from bson import ObjectId
from helpers.exceptions import ValidationException
from services.database import mongo_database
from werkzeug.security import generate_password_hash, check_password_hash

mongo_collection = mongo_database.get_collection('users')


class UserService:
    @staticmethod
    def verify_password(username: str, password: str) -> str:
        found_user = mongo_collection.find_one({
            'username': username
        })

        if not found_user:
            raise ValidationException('Invalid username/password')

        if not check_password_hash(found_user.get('password'), password):
            raise ValidationException('Invalid username/password')

        return str(found_user.get('_id'))

    @staticmethod
    def register_user(username: str, password: str):
        found_user = mongo_collection.find_one({
            'username': username
        })

        if found_user:
            raise ValidationException('Username already exists')

        hashed_pass = generate_password_hash(password)

        mongo_collection.insert_one({
            'username': username,
            'password': hashed_pass,
            'roles': ['default']
        })

    @staticmethod
    def get_by_id(user_id: str) -> str:
        return mongo_collection.find_one({
            '_id': ObjectId(user_id)
        })

    @staticmethod
    def get_roles_by_id(user_id: str) -> str:
        return mongo_collection.find_one({
            '_id': ObjectId(user_id)
        },
        {
            'roles': 1
        })