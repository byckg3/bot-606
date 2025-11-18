from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field
from web.hyl.models import CheckInTask

class ProgressMetaData( BaseModel ):
    task_name: CheckInTask | str = ""
    date: str | None = None

class DailyProgress( BaseModel ):
    title: str = ""
    progress: str = ""
    metadata: ProgressMetaData = Field( default_factory = ProgressMetaData )
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    
    model_config = ConfigDict( extra = "ignore" )