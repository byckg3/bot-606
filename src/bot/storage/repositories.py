import pymongo
from pymongo.database import Database
from datetime import datetime, timezone
from bson import ObjectId
from bot.storage.core.dbs import RedisDB
from bot.storage.models.mappers import ProgressMapper
from bot.storage.models.progress import DailyProgress

class CheckInProgressRepository:
    
    collection_name = "daily_progress"
    timeField_name = "created_at"
    metaField_name = "metadata"
    
    def __init__( self, db: Database ):
        if self.collection_name not in db.list_collection_names():
            
            db.create_collection(
                self.collection_name,
                timeseries={
                    "timeField": self.timeField_name,
                    "metaField": self.metaField_name, 
                },
                expireAfterSeconds = 3 * 24 * 60 * 60, # 3 days
                check_exists = True, )
        
        self.collection = db.get_collection( self.collection_name )
        

    def insert( self, dp: DailyProgress ) -> str:
        current_utc = datetime.now( timezone.utc )
        
        dp.updated_at = current_utc
        dp.created_at = current_utc
        
        progress_doc = ProgressMapper.to_doc( dp )
        try:
            result = self.collection.insert_one( progress_doc )
            if not result.inserted_id:
                raise RuntimeError( "no inserted_id returned" )
            
            return str( result.inserted_id )
            
        except Exception as e:
            raise RuntimeError( "Failed to insert progress" ) from e
        
        
    def find_by( self, condition: dict[ str, str ], last_id: ObjectId | None = None, limit: int = 20 ) -> list[ DailyProgress ]:
        
        query: dict = {}
        if "date" in condition:
            query[ "metadata.date" ] = condition[ "date" ]
            
        if "task_code" in condition:
            query[ "metadata.task_code" ] = condition[ "task_code" ]
        
        if last_id:
            query[ "_id" ] = { "$gt": last_id }
        
        try:
            results = self.collection.find( query ) \
                                     .sort( "created_at", pymongo.DESCENDING ) \
                                     .limit( limit )
                                     
            return [ ProgressMapper.to_model( result ) for result in results ]
        
        except Exception as e:
            raise RuntimeError( "Failed to find progress" ) from e

    def update( self, query_filter: dict, content: dict ) -> int:
        try:
            query = ProgressMapper.to_doc_filters( query_filter )
            updated = ProgressMapper.to_doc_filters( content )
            result = self.collection.update_many( query, { "$set": updated } )
            
            return result.modified_count
        
        except Exception as e:
            raise RuntimeError( "Failed to update progress" ) from e


    def delete( self, query_filter: dict ) -> int:
        try:
            query = ProgressMapper.to_doc_filters( query_filter )
            result = self.collection.delete_many( query )
            
            return result.deleted_count
        
        except Exception as e:
            raise RuntimeError( "Failed to delete progress" ) from e
        

class ConfigRepository:
    
    collection_name = "configurations"
    
    def __init__( self, db: Database ):
        
        if self.collection_name not in db.list_collection_names():
            db.create_collection( self.collection_name )
        
        self.collection = db.get_collection( self.collection_name )
        
    
    def save_config( self, key: str, config: dict ) -> str:
        try:
            result = self.collection.update_one(
                { "name": key },
                { "$set": config },
                upsert = True 
            )
            
            if result.upserted_id:
                return str( result.upserted_id )
            else:
                return ""
        
        except Exception as e:
            raise RuntimeError( "Failed to save configuration" ) from e
        
        
    def get_config( self, key: str ) -> dict | None:
        try:
            result = self.collection.find_one( { "name": key } )
            
            if result:
                return result
            else:
                return None
        
        except Exception as e:
            raise RuntimeError( "Failed to get configuration" ) from e
        

class CacheRepository:
    
    def __init__( self, redis_client, prefix: str = "bot606:cache:" ):
        self.client = redis_client
        self.key_prefix = prefix
        
    
    def set( self, key: str, value: str, expire_seconds: int = 3600 ) -> None:
        full_key = self.key_prefix + key
        
        return self.client.set( full_key, value, ex = expire_seconds )
        
        
    def get( self, key: str ) -> str | None:
        full_key: str = self.key_prefix + key
        
        value = self.client.get( full_key )
        if value is not None:
            return value
        
        return None