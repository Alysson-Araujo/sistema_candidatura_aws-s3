import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import settings
import logging
from typing import Optional
from io import BytesIO

class S3Service:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        session = boto3.Session(profile_name=settings.aws_profile_name)
        self.s3_client = session.client("s3")
        
        self.bucket_name = settings.aws_bucket_name
        
    def upload_file(self, file: BytesIO, object=None) -> Optional[str]:
        if object is None:
            raise ValueError("O nome do objeto deve ser fornecido.")
        
        try:
            self.s3_client.upload_fileobj(
                file, self.bucket_name, object
            )
            logging.info(f"Arquivo {file} enviado com sucesso para o bucket {self.bucket_name}")
            
            return f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{object}"
        except (BotoCoreError, ClientError) as e:
            logging.error(f"Erro ao fazer upload do arquivo {file}: {e}")
            return None
