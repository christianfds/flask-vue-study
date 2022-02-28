import datetime
from xmlrpc.client import boolean
from bson import ObjectId
from services.database import mongo_database

mongo_collection = mongo_database.get_collection('photos')
mongo_reaction_collection = mongo_database.get_collection('reactions')


# class PhotoModel:
    # _id: str
    # uploaded_by: ObjectId
    # status: ['pending', 'accepted', 'rejected']
    # deleted: False
    # analysed_by: ObjectId
    # title: str
    # image_uri: str
    # created_at: datetime.datetime



class PhotosService:
    @staticmethod
    def list_photos(status: str = 'accepted', user_id: str = '',  page: int = 0, page_size: int = 20) -> list[dict]:
        result = mongo_collection.aggregate([
            {
                '$match': {'status': status, 'deleted': False}
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'comments.user_id',
                    'foreignField': '_id',
                    'as': 'commenter_info'
                }
            },
            {
                '$lookup': {
                    'from': 'reactions',
                    'pipeline': [
                        { '$match': { 'user_id': ObjectId(user_id) } }
                    ],
                    'localField': '_id',
                    'foreignField': 'photo_id',
                    'as': 'my_reactions'
                }
            },
            {
                '$lookup': {
                    'from': 'reactions',
                    'localField': '_id',
                    'foreignField': 'photo_id',
                    'as': 'all_reactions'
                }
            },
            {
                '$addFields': {
                    'comment_count': {'$size': '$comments'},
                    'like_count': {'$size': '$all_reactions'},
                    'i_liked': {
                        '$cond': [{'$gt': [{'$size': '$my_reactions'}, 0]}, True, False]
                    }
                }
            },
            {
                '$project': {
                    'my_reactions': 0,
                    'all_reactions': 0
                }
            },
            {
                '$sort': {'created_at': -1}
            },
            # {
            #     '$skip': page * page_size
            # },
            # {
            #     '$limit': page_size
            # }
        ])

        # Parses id to string
        result = [
            {
                **r,
                '_id': str(r['_id']),
                'uploaded_by': str(r['uploaded_by']),
                'analysed_by': str(r['analysed_by']),
                'comments': [
                    {
                        **c,
                        'user_id': str(c['user_id']),
                        'username': [u['username'] for u in r['commenter_info'] if u['_id'] == c['user_id']][0]
                    }
                    for c in r['comments']
                ]
            } for r in result
        ]

        for r in result:
            r.pop('commenter_info')
            if r['analysed_by'] == '' or r['analysed_by'] == 'None' or r['analysed_by'] is None:
                r.pop('analysed_by')

        return list(result)

    @staticmethod
    def get_photo_details(photo_id: str) -> dict:
        result = mongo_collection.find_one({
            '_id': ObjectId(photo_id),
            'status': 'accepted',
            'deleted': False
        })

        if result:
            result = {
                **result,
                '_id': str(result['_id'])
            }

        return result
    
    @staticmethod
    def submit_photo(uploader_id: str, title: str, image_uri: str):
        mongo_collection.insert_one({
            'uploaded_by': ObjectId(uploader_id),
            'status': 'pending',
            'deleted': False,
            'analysed_by': None,
            'title': title,
            'comments': [],
            'image_uri': image_uri,
            'created_at': datetime.datetime.utcnow(),
        })

    @staticmethod
    def avaliate_photo(avaliator_id: str, photo_id: str, avaliation: str):
        assert avaliation in ['accepted', 'rejected']

        mongo_collection.update_one({
            '_id': ObjectId(photo_id)
        },
        {
            '$set': {
                'status': avaliation,
                'analysed_by': ObjectId(avaliator_id)
            }
        })

    @staticmethod
    def set_reaction(photo_id: str, user_id: str, active: boolean = True, reaction_type: str = 'like'):
        object_filter = {
            'photo_id': ObjectId(photo_id),
            'user_id': ObjectId(user_id),
            'reaction_type': reaction_type
        }
        reaction = mongo_reaction_collection.find_one(object_filter)

        if active:
            if not reaction:
                mongo_reaction_collection.insert_one(
                    object_filter
                )

        else:
            if reaction:
                mongo_reaction_collection.delete_one(
                    object_filter
                )

    @staticmethod
    def add_comment(photo_id: str, user_id: str, message: str):
        comment = {
            'user_id': ObjectId(user_id),
            'message': message,
            'created_at': datetime.datetime.utcnow()
        }

        mongo_collection.update_one({
            '_id': ObjectId(photo_id)
        },
        {
            '$push': {
                'comments': {
                    'user_id': ObjectId(user_id),
                    'message': message
                }
            }
        })

        comment = {
            **comment,
            'user_id': user_id
        }
        return comment
