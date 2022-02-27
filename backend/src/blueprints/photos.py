from lib2to3.pgen2 import token
import logging
from flask import Blueprint, request
from blueprints.auth import get_current_user
from helpers.response import DefaultResponse
from services.photos import PhotosService
from services.aws import AWSService
from services.session import token_auth

logger = logging.getLogger('gallery.photos')
logger.setLevel(logging.INFO)

photos_app = Blueprint('photos_app', __name__)


@photos_app.route('/', methods=['GET'])
@token_auth.login_required
def list_photos():
    page = request.args.get('page', 0)
    page_size = request.args.get('page_size', 20)
    try:
        photos = PhotosService.list_photos(page=page, page_size=page_size)
        return DefaultResponse.success_response('Found photos', photos)
    except Exception as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.internal_failed_response()


@photos_app.route('/', methods=['POST'])
@token_auth.login_required
def submit_photo():
    user = get_current_user()

    data = request.json
    try:
        title = data['title']
        file_data = data['file']['data']

        image_url = AWSService.submit_file_from_base64(file_data)
        PhotosService.submit_photo(user['_id'], title, image_url)

        return DefaultResponse.success_response('File upload successfully')
    
    except KeyError as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.failed_response(f'Missing `{e}`')

    except Exception as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.internal_failed_response()


# Admin and non-Admin
@photos_app.route('/<string:photo_id>', methods=['DELETE'])
@token_auth.login_required
def delete_photo(photo_id: str):
    pass


@photos_app.route('/<string:photo_id>', methods=['GET'])
@token_auth.login_required
def get_photo_with_details(photo_id: str):
    try:
        photo = PhotosService.get_photo_details(photo_id)
        if not photo:
            return DefaultResponse.failed_response('Photo not found', status=400)
        return DefaultResponse.success_response('Found photo', photo)
    except Exception as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.internal_failed_response()


@photos_app.route('/<string:photo_id>/comment', methods=['POST'])
@token_auth.login_required
def add_comment(photo_id: str):
    pass


@photos_app.route('/<string:photo_id>/comment/<string:comment_id>', methods=['DELETE'])
@token_auth.login_required(role='admin')
def delete_comment(photo_id: str, comment_id: str):
    # Comment index with `deleted` flag
    pass


@photos_app.route('/<string:photo_id>/react', methods=['POST'])
@token_auth.login_required
def add_reaction(photo_id: str):
    pass


@photos_app.route('/pending', methods=['GET'])
@token_auth.login_required(role='admin')
def list_pending_photos():
    page = request.args.get('page', 0)
    page_size = request.args.get('page_size', 20)
    try:
        photos = PhotosService.list_photos(status='pending', page=page, page_size=page_size)
        return DefaultResponse.success_response('Found photos', photos)
    except Exception as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.internal_failed_response()
    

@photos_app.route('/pending/<string:photo_id>', methods=['POST'])
@token_auth.login_required(role='admin')
def avaliate_photo(photo_id):
    user = get_current_user()

    data = request.json
    logger.debug(data)
    try:
        photos = PhotosService.avaliate_photo(user['_id'], photo_id, data['status'])
        return DefaultResponse.success_response('Found photos', photos)
    
    except KeyError as e:
        logger.error(e, exc_info= True)
        return DefaultResponse.failed_response(f'Missing `{e}`')
    
    except Exception as e:
        logger.error(e, exc_info=True)
        return DefaultResponse.internal_failed_response()
