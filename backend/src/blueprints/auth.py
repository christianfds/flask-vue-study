import logging
from flask import Blueprint, request, g
from services.session import SessionService, token_auth

from helpers.exceptions import ValidationException
from helpers.response import DefaultResponse
from services.user import UserService

logger = logging.getLogger('gallery.auth')
logger.setLevel(logging.INFO)


auth_app = Blueprint('auth_app', __name__)


@auth_app.route('/', methods=['POST'])
def login():
    data = request.json
    logger.debug(data)
    try:
        if 'username' not in data:
            raise ValidationException('Missing username')

        if 'password' not in data:
            raise ValidationException('Missing password')

        user = UserService.verify_password(data.get('username'), data.get('password'))
        token = SessionService.insert_token(user['_id'])
        
        return DefaultResponse.success_response('Login successful', {
            **user,
            'token': token
        })

    except ValidationException as e:
        return DefaultResponse.failed_response(str(e))

    except BaseException:
        logger.error('', exc_info=True)
        return DefaultResponse.internal_failed_response()


@auth_app.route('/register', methods=['POST'])
def register():
    data = request.json
    logger.debug(data)
    try:
        if 'username' not in data:
            raise ValidationException('Missing username')

        if 'password' not in data:
            raise ValidationException('Missing password')

        UserService.register_user(data.get('username'), data.get('password'))

        return DefaultResponse.success_response('User created')

    except ValidationException as e:
        return DefaultResponse.failed_response(str(e), e.status)

    except BaseException:
        logger.error('', exc_info=True)
        return DefaultResponse.internal_failed_response()


@auth_app.route('/', methods=['DELETE'])
@token_auth.login_required
def logout():
    token = token_auth.get_auth()
    SessionService.destroy_token(token.get('token'))
    return DefaultResponse.success_response('Logout successful')


@auth_app.route('/', methods=['GET'])
@token_auth.login_required(role='admin')
def whoami():
    user = get_current_user()
    return DefaultResponse.success_response(data=user)


@token_auth.verify_token
def verify_token(token: str):
    user = SessionService.check_token(token)
    if user:
        g.flask_httpauth_user = user
        return user
    else:
        return False

@token_auth.get_user_roles
def get_user_roles(user):
    return user.get('roles', [])

def get_current_user():
    if hasattr(g, 'flask_httpauth_user'):
        return g.flask_httpauth_user