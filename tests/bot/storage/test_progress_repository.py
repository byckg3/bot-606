import pytest
from datetime import date
from bot.storage.core.config import mongodb_settings
from bot.storage.core.dbs import MongoDB
from bot.storage.models.progress import DailyProgress
from bot.storage.repositories import CheckInProgressRepository

@pytest.fixture( scope = "class" )
def progress_repository():
    
    connection = MongoDB( mongodb_settings().URI )
    test_db = connection.database( "test" )
    
    print( "\nSetup CheckInProgressRepository for tests" )
    progress_repository = CheckInProgressRepository( test_db )
    
    yield progress_repository
    
    progress_repository.delete( 
        { "task_code": { "$regex": TestCheckInProgressRepository.task, 
                         "$options": "i" } 
        } 
    )
    print( "\nTeardown CheckInProgressRepository for tests" )
    
    connection.close()


@pytest.mark.db
class TestCheckInProgressRepository:
    
    today: str = str( date.today() )  # Current local date
    task: str = "test"
    
    def test_insert_progress( self, progress_repository ):
        
        dp = DailyProgress.model_validate(
            { 
                "progress": "第 N 天",
                "title": "每日簽到",
                "task_code": self.task, 
                "date": self.today,
            } 
        )
        inserted_id = progress_repository.insert( dp )
        # print( f"\nInserted ID: {inserted_id}" )
        
        assert inserted_id is not None
    
    def test_find_progress( self, progress_repository: CheckInProgressRepository ):
        results = progress_repository.find_by( { "date": self.today }, limit = 1 )
        # print( results )
        
        assert len( results ) > 0
        assert results[ 0 ].date == self.today
    
    
    # https://www.mongodb.com/docs/upcoming/core/timeseries/timeseries-limitations/
    def test_update_progress( self, progress_repository ):
        query_filter = { 
            "date": self.today
        }
        update_operation = {
            "task_code": "updated_" + self.task,
        }
        
        modified_count = progress_repository.update( query_filter,
                                                     update_operation )
        # print( f"\nModified count: {modified_count}" )
        
        assert modified_count > 0
    
        
    def test_delete_progress( self, progress_repository ):
        deleted_count = progress_repository.delete( 
            { 
                "date": self.today,
            } 
        )
        # print( f"\nDeleted count: {deleted_count}" )
        
        assert deleted_count > 0
        
    
    