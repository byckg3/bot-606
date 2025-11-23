from datetime import datetime, timezone
from enum import StrEnum, auto
from pydantic import BaseModel, Field

class CheckinResult( BaseModel ):
    title: str
    page_url: str
    progress: str
    status: str = "failed"
    date: str = ""
    
class CheckInTask( StrEnum ):
    GSI = auto() # "gsi"
    ZZZ = auto() # "zzz"
    HSR = auto() # "hsr"