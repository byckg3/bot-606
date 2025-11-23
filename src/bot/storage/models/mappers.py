from bot.storage.models.progress import DailyProgress

class ProgressMapper:
    
    @staticmethod
    def to_model( doc: dict ) -> DailyProgress:
        dp = DailyProgress.model_validate( doc )
        
        metadata = doc.get( "metadata", {} )
        dp.date = metadata.get( "date", "" )
        dp.task_code = metadata.get( "task_code", "" )
        
        return dp
    
    @staticmethod
    def to_doc( dp: DailyProgress ) -> dict:
        doc = dp.model_dump()
        doc[ "metadata" ] = {
            "task_code": doc.pop( "task_code", "" ),
            "date": doc.pop( "date", "" )
        }
        
        return doc
    
    @staticmethod
    def to_doc_fields( query: dict ) -> dict:
        transformed_query = {}
        
        for key, value in query.items():
            if key in [ "date", "task_code" ]:
                transformed_key = f"metadata.{key}"
            else:
                transformed_key = key
            
            transformed_query[ transformed_key ] = value
        
        return transformed_query