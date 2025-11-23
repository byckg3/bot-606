from bot.storage.models.progress import DailyProgress
from bot.storage.repositories import CheckInProgressRepository

class ProgressService:
    
    def __init__( self, repository: CheckInProgressRepository ):
        self.repository = repository
        
        
    def save_progress( self, progress: DailyProgress ):
        return self.repository.insert( progress )
    
    
    def get_last_progress( self, task_code: str ) -> DailyProgress:
        
        query = { "task_code": task_code }
        results = self.repository.find_by( query, limit = 1 )
        
        if results:
            return results[ 0 ]
        else:
            return DailyProgress()