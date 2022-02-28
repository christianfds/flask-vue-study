from ast import Bytes
from io import BytesIO
import boto3
from itsdangerous import base64_decode
from config import config
import hashlib
import base64
from mimetypes import guess_extension, guess_type

session = boto3.Session(
    aws_access_key_id=config.get('aws').get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config.get('aws').get('AWS_SECRET_ACCESS_KEY'),
)

class AWSService:
    @staticmethod
    def submit_file_from_base64(file_base64: str) -> str:
        extension = guess_extension(guess_type(file_base64)[0])

        # Encode base64 data        
        encoded_file = file_base64.split('base64,', 1)[1].encode('utf-8')

        # Generate the file name using the md5 and the mime extension
        md5sum = hashlib.md5(encoded_file).hexdigest()
        file_path = ''.join([md5sum, extension])
        
        # Write the data to a bytes IO
        file_data = BytesIO()
        decoded_image = base64.decodebytes(encoded_file)
        file_data.write(decoded_image)
        file_data.seek(0)

        # Upload it to s3
        bucket_name = config.get('aws').get('AWS_BUCKET')
        session.client('s3').upload_fileobj(
            file_data,
            bucket_name,
            file_path
        )

        return AWSService.get_public_link(file_path)
        
    @staticmethod
    def get_public_link(object_key: str) -> str:
        bucket_name = config.get('aws').get('AWS_BUCKET')

        bucket_location = session.client('s3').get_bucket_location(Bucket=bucket_name)
        return "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            bucket_name,
            object_key
        )