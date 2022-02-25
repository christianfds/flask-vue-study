import os

config = {
    'mongo': {
        'uri': f"""mongodb://{os.environ.get('MONGODB_USER')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOST')}""",
        'default_database': 'gallery'
    },
    'jwt': {
        'secret_key': os.environ.get('JWT_SECRET_KEY', 'guess_who')
    }
}
