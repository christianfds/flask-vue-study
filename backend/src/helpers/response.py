from flask import make_response


class DefaultResponse():
    @staticmethod
    def success_response(message: str = '', data: dict[any] = {}, status: int = 200):
        default = {
            'success': True,
            'message': message,
            'data': data
        }
        resp = make_response(default)

        return resp, status

    @staticmethod
    def failed_response(message: str = '', status: int = 400):
        default = {
            'success': False,
            'message': message,
        }
        resp = make_response(default)

        return resp, status

    @staticmethod
    def internal_failed_response(message: str = 'Internal error', status: int = 500):
        default = {
            'success': False,
            'message': message,
        }
        resp = make_response(default)

        return resp, status
