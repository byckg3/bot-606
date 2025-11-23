from __future__ import annotations
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field
from web.hyl.models import CheckInTask

class DailyProgress( BaseModel ):
    
    date: str = ""
    title: str = ""
    progress: str = ""
    task_code: CheckInTask | str = ""
      
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    
    model_config = ConfigDict( extra = "ignore" )