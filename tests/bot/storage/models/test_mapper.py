import pytest
from bot.storage.models.mappers import ProgressMapper
from bot.storage.models.progress import DailyProgress

@pytest.fixture( scope = "class" )
def dp_doc():
    return {
        "title": "test title",
        "progress": "第 10 天",
        "metadata": {
            "task_code": "test",
            "date": "2024-06-15",
        }
    }

@pytest.fixture( scope = "class" )
def dp_model():
    dp = {
        "title": "test title",
        "progress": "第 10 天",
        "task_code": "test",
        "date": "2024-06-15",
    }
    return DailyProgress.model_validate( dp )

class TestProgressMapper:
    
    
    def test_map_to_doc( self, dp_model, dp_doc ):
        actual_doc = ProgressMapper.to_doc( dp_model )
        
        assert actual_doc[ "title" ] == dp_doc[ "title" ]
        assert actual_doc[ "progress" ] == dp_doc[ "progress" ]
        assert actual_doc[ "metadata" ] == dp_doc[ "metadata" ]
        
        
    def test_map_to_model( self, dp_model, dp_doc ):
       
        actual_model = ProgressMapper.to_model( dp_doc )
        
        assert actual_model.title == dp_model.title
        assert actual_model.progress == dp_model.progress
        assert actual_model.task_code == dp_model.task_code
        assert actual_model.date == dp_model.date
        

    def test_map_to_doc_fields( self ):
        query = {
            "task_code": "test",
            "date": "2024-06-15",
            "title": "test title",
        }
        actual_transformed_query = ProgressMapper.to_doc_filters( query )
        expected_transformed_query = {
            "metadata.task_code": "test",
            "metadata.date": "2024-06-15",
            "title": "test title",
        }
        
        assert actual_transformed_query == expected_transformed_query