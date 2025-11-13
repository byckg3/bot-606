from datetime import date, datetime, timezone
from bson import ObjectId
from pymongo.database import Database
from pymongo.results import InsertOneResult

class CheckInProgressRepository:
    
    COLLECTION_NAME = "daily_progress"
    
    def __init__( self, db: Database ):
        if self.COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(
                self.COLLECTION_NAME,
                timeseries={
                    "timeField": "created_at",
                    "metaField": "metadata", 
                },
                expireAfterSeconds = 3 * 24 * 60 * 60, # 3 days
                check_exists = True, )
        
        self.collection = db.get_collection( self.COLLECTION_NAME )
        

    def insert( self, progress: dict ):
        current_utc = datetime.now( timezone.utc )
        
        progress[ "updated_at" ] = current_utc
        progress[ "created_at" ] = current_utc
        
        try:
            result = self.collection.insert_one( progress )
            if not result.inserted_id:
                raise RuntimeError( "no inserted_id returned" )
            
            return str( result.inserted_id )
            
        except Exception as e:
            raise RuntimeError( "Failed to insert progress" ) from e
        
        
    def find( self, query: dict, last_id: ObjectId | None = None, limit: int = 20 ):
        if last_id:
            query[ "_id" ] = { "$gt": last_id }
        
        try:
            results = self.collection.find( query ).limit( limit )
            return list( results )
        
        except Exception as e:
            raise RuntimeError( "Failed to find progress" ) from e


    def delete( self, query: dict ):
        try:
            result = self.collection.delete_many( query )
            return result.deleted_count
        
        except Exception as e:
            raise RuntimeError( "Failed to delete progress" ) from e
        
        
    def update( self, query_filter: dict, update: dict ):
        try:
            result = self.collection.update_many( query_filter, { "$set": update } )
            return result.modified_count
        
        except Exception as e:
            raise RuntimeError( "Failed to update progress" ) from e