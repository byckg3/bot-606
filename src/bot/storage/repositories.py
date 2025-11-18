from datetime import datetime, timezone
from bson import ObjectId
from pymongo.database import Database
from pymongo.results import InsertOneResult
from bot.storage.models import DailyProgress

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
        

    def insert( self, progress: DailyProgress ) -> str:
        current_utc = datetime.now( timezone.utc )
        
        progress.updated_at = current_utc
        progress.created_at = current_utc
        
        try:
            result = self.collection.insert_one( progress.model_dump() )
            if not result.inserted_id:
                raise RuntimeError( "no inserted_id returned" )
            
            return str( result.inserted_id )
            
        except Exception as e:
            raise RuntimeError( "Failed to insert progress" ) from e
        
        
    def find( self, query: dict, last_id: ObjectId | None = None, limit: int = 20 ) -> list[ DailyProgress ]:
        if last_id:
            query[ "_id" ] = { "$gt": last_id }
        
        try:
            results = self.collection.find( query ) \
                                     .sort( "created_at", -1 ) \
                                     .limit( limit )
            return [ DailyProgress.model_validate( result ) for result in results ]
        
        except Exception as e:
            raise RuntimeError( "Failed to find progress" ) from e


    def delete( self, query: dict ) -> int:
        try:
            result = self.collection.delete_many( query )
            return result.deleted_count
        
        except Exception as e:
            raise RuntimeError( "Failed to delete progress" ) from e
        
        
    def update( self, query_filter: dict, update: dict ) -> int:
        try:
            result = self.collection.update_many( query_filter, { "$set": update } )
            return result.modified_count
        
        except Exception as e:
            raise RuntimeError( "Failed to update progress" ) from e
        

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