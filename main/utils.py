import boto3
from botocore.exceptions import ClientError, ParamValidationError
import os

class AWS:

    def __init__(self, aws_access_key_id,  aws_secret_access_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def get_file_from_aws(self, filename, S3_BUCKET, expiresIn=20):
        """
        brings a file from AWS S3 bucket
        returns :
            image URL : if file is catched,
            None : if file is not downloaded
        """
        try:
            s3 = boto3.client(
                's3',  aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
              )

            img_url = s3.generate_presigned_url(
                'get_object',
                Params = {'Bucket': S3_BUCKET, 'Key': filename},
                ExpiresIn = expiresIn,
            )

            return img_url
            download_status = True

        except s3.exceptions.NoSuchBucket as exception:
            download_status = False
            exception_message = " bucket doesn't exist"
            exception_details = f"NoSuchBucket Error: {exception}"

        except ParamValidationError as exception:
            download_status = False
            exception_message = "Parameter validation error"
            exception_details = f"Parameter validation error: {exception}"

        except ClientError as exception:
            download_status = False
            exception_message = " Unexpected error"
            exception_details = f"Unexpected error(ClientError): {exception}"

        return {
            "download_status": download_status,
            "exception_message": exception_message,
            "exception_details": exception_details,
         }

    def upload_image_or_mp3_to_aws(self, filename, img_data, S3_BUCKET, contet_type='image', **kwargs):
        """
        uploading an image or an mp3 file to aws s3 server
        (made originaly for maptlotlib images)
        """

        if contet_type == "image":
            contentType = "image/png"
        elif content_type == "mp3":
            contentType = "audio/mp3"

        try:
            # img_data.seek(0)
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )

            s3.put_object(
                Body=img_data,
                ContentType=contentType,
                Key=filename,
                Bucket=S3_BUCKET,
                **kwargs
            )

            uploading_status = True
            exception_message = None
            exception_details = None

        # except s3.exceptions.NoSuchBucket as exception:
        #     uploading_status = False
        #     exception_message = "bucket doesn't exist"
        #     exception_details = f"NoSuchBucket Error: {exception}"

        # except s3.exceptions.EntityAlreadyExistsException as exception:
        #     uploading_status = False
        #     exception_message = "there is a file with this name that already exists"
        #     exception_details = f"EntityAlreadyExistsException Error: {exception}"

        except ParamValidationError as exception:
            uploading_status = False
            exception_message = "Parameter validation error"
            exception_details = f"Parameter validation error: {exception}"

        except ClientError as exception:
            uploading_status = False
            exception_message = "Unexpected error"
            exception_details = f"Unexpected error(ClientError): {exception}"

        return {
            "uploading_status": uploading_status,
            "exception_message": exception_message,
            "exception_details": exception_details,
         }
