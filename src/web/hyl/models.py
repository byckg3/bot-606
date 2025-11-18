from datetime import datetime, timezone
from enum import StrEnum, auto
from pydantic import BaseModel, Field

class CheckinResult( BaseModel ):
    title: str
    page_url: str
    progress: str
    status: str = "failed"
    date: str | None = None
    created_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    updated_at: datetime = Field( default_factory = lambda: datetime.now( timezone.utc ) )
    
class CheckInTask( StrEnum ):
    GSI = auto() # "gsi"
    ZZZ = auto() # "zzz"
    HSR = auto() # "hsr"