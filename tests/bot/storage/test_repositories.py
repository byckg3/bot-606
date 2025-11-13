import pytest
from datetime import date, datetime, timezone
from bot.config import mongodb_settings
from bot.storage.db import MongoDB
from bot.storage.repositories import CheckInProgressRepository

@pytest.fixture( scope = "class" )
def progress_repository():
    
    connection = MongoDB( mongodb_settings().URI )
    test_db = connection.database( "test" )
    
    print( "\nSetup CheckInProgressRepository for tests" )
    progress_repository = CheckInProgressRepository( test_db )
    
    yield progress_repository
    
    progress_repository.delete( 
        { "metadata.task_name": { "$regex": TestCheckinProgressRepository.task, 
                                  "$options": "i" } 
        } 
    )
    print( "\nTeardown CheckInProgressRepository for tests" )
    
    connection.close()


@pytest.mark.db
class TestCheckinProgressRepository:
    
    today: str = str( date.today() )  # Current local date
    task: str = "test"
    
    def test_insert_progress( self, progress_repository ):
        inserted_id = progress_repository.insert(
            { 
                "progress": "第 N 天",
                "title": "每日簽到",
                "metadata": { 
                    "task_name": self.task, 
                    "date": self.today,
                }
            } 
        )
        # print( f"\nInserted ID: {inserted_id}" )
        
        assert inserted_id is not None
    
    
    def test_find_progress( self, progress_repository ):
        results = progress_repository.find( { "metadata.date": self.today } )
        # print( results )
        
        assert len( results ) > 0
        assert results[ 0 ][ "metadata" ][ "date" ] == self.today
    
    
    # https://www.mongodb.com/docs/upcoming/core/timeseries/timeseries-limitations/
    def test_update_progress( self, progress_repository ):
        query_filter = { 
            "metadata.date": self.today
        }
        update_operation = {
            "metadata.task_name": "updated_" + self.task,
        }
        
        modified_count = progress_repository.update( query_filter,
                                                     update_operation )
        # print( f"\nModified count: {modified_count}" )
        
        assert modified_count > 0
    
        
    def test_delete_progress( self, progress_repository ):
        deleted_count = progress_repository.delete( 
            { 
                "metadata.date": self.today,
            } 
        )
        # print( f"\nDeleted count: {deleted_count}" )
        
        assert deleted_count > 0
        
    
    