from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_bucket_name: str
    aws_region: str
    aws_profile_name: str
    
    mongodb_uri: str
    mongodb_db_name: str
    mongodb_collection_name: str
    
    class Config:
        env_file = ".env"


settings = Settings()
