import datetime
from bson import ObjectId
from services.database import mongo_database

mongo_collection = mongo_database.get_collection('photos')


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
    def list_photos(status: str = 'accepted', page: int = 0, page_size: int = 20) -> list[dict]:
        result = mongo_collection.aggregate([
            {
                '$match': {'status': status, 'deleted': False}
            },
            {
                '$sort': {'created_at': -1}
            },
            {
                '$skip': page * page_size
            },
            {
                '$limit': page_size
            }
        ])

        # Parses id to string
        result = [{**r, '_id': str(r['_id'])} for r in result]
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

