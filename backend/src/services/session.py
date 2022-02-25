import jwt
import datetime
from config import config
from bson import ObjectId
from flask_httpauth import HTTPTokenAuth
from services.database import mongo_database

# Token auth
token_auth = HTTPTokenAuth('Bearer')

mongo_collection = mongo_database.get_collection('users')
JWT_SECRET_KEY = config.get('jwt').get('secret_key')

class SessionService:
    @staticmethod
    def _generate_token(user_id: str) -> str:
        return jwt.encode(
            {
                'user_id': user_id,
                'creation_date': str(datetime.datetime.utcnow())
            },
            JWT_SECRET_KEY
        )

    @staticmethod
    def destroy_token(token: str):
        user = mongo_collection.find_one({
            'token': token
        })

        if user:
            mongo_collection.update_one(
                {
                    '_id': user.get('_id')
                },
                {
                    '$unset': {
                        'token': 1
                    }
                }
            )

    @staticmethod
    def check_token(token: str) -> str:
        user = mongo_collection.find_one({
            'token': token
        })

        if user and '_id' in user:
            user['_id'] = str(user['_id'])

        return  user

    @staticmethod
    def insert_token(user_id: str) -> str:
        jwt_token = SessionService._generate_token(user_id)

        mongo_collection.update_one({
            '_id': ObjectId(user_id)
        },
        {
            '$set': {
                'token': jwt_token
            }
        })

        return jwt_token