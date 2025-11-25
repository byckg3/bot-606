import pytest
from bot.storage.core.config import redis_settings
from bot.storage.core.dbs import RedisDB
from bot.storage.models.progress import DailyProgress
from bot.storage.repositories import CacheRepository

@pytest.fixture( scope = "class" )
def cache_repository():
    
    redis = RedisDB( redis_settings().URI )
    cache_repository = CacheRepository( redis.client, "test:cache:" )
   
    yield cache_repository
    
    redis.close()
    
    
class TestCacheRepository:
    
    @pytest.mark.target
    def test_set_and_get_cache( self, cache_repository ):
        key = "test_key"
        dp = DailyProgress.model_validate(
            {
                "title": "test title",
                "progress": "第 10 天",
                "task_code": "test",
                "date": "2024-06-15",
            }
        )
        value = dp.model_dump_json()
        # print( f"\nCached value: {value}" )
        
        cache_repository.set( key, value )
        retrieved_value = cache_repository.get( key )
        # print( f"\nRetrieved value: {retrieved_value}" )
        
        assert retrieved_value == value