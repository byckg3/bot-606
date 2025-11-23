from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class MongoDBSettings( BaseSettings ):

    URI: str
    DB_NAME: str
    COLLECTION_NAME: str

    model_config = SettingsConfigDict( 
        env_file = ".env", 
        env_file_encoding = "utf-8",
        env_prefix = "MONGO_",
        extra = "ignore",
    )
    
class RedisSettings( BaseSettings ):

    URI: str

    model_config = SettingsConfigDict( 
        env_prefix = "REDIS_",
        extra = "ignore",
    )
    

@lru_cache()
def mongodb_settings():
    return MongoDBSettings() # type: ignore

# print( mongodb_settings().model_dump() )

@lru_cache()
def redis_settings():
    return RedisSettings() # type: ignore