import os

config = {
    'mongo': {
        'uri': f"""mongodb://{os.environ.get('MONGODB_USER')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOST')}""",
        'default_database': 'gallery'
    },
    'jwt': {
        'secret_key': os.environ.get('JWT_SECRET_KEY', 'guess_who')
    },
    'aws': {
        'AWS_BUCKET': os.environ.get('AWS_BUCKET'),
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
    }
}

