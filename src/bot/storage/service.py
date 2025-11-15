from bot.storage.repositories import CheckInProgressRepository

class ProgressService:
    
    def __init__( self, repository: CheckInProgressRepository ):
        self.repository = repository
        
        
    def save_progress( self, progress: dict ):
        return self.repository.insert( progress )
    
    
    def get_last_progress( self, task_name: str ):
        
        query = { "metadata.task_name": task_name }
        results = self.repository.find( query, limit = 1 )
        
        if results:
            return results[ 0 ]
        else:
            return {}