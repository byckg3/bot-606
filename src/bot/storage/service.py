from bot.storage.models.progress import DailyProgress
from bot.storage.repositories import CacheRepository, CheckInProgressRepository

class ProgressService:
    
    def __init__( self, progress_repo: CheckInProgressRepository, 
                        cache_repo: CacheRepository ):
        self.progress_repository = progress_repo
        self.cache_repository = cache_repo
        
        
    def save_progress( self, progress: DailyProgress ):
        self.progress_repository.insert( progress )
        return self.cache_repository.set( progress.task_code, progress.model_dump_json() )
    
    
    def get_last_progress( self, task_code: str ) -> DailyProgress:
        
        cached = self.cache_repository.get( task_code )
        if cached is not None:
            return DailyProgress.model_validate_json( cached )
        
        query = { "task_code": task_code }
        results = self.progress_repository.find_by( query, limit = 1 )
        if not results:
            return DailyProgress()
            
        last = results[ 0 ]
        self.cache_repository.set( task_code, last.model_dump_json() )
        
        return last