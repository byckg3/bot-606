from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml

class CheckInPageSettings( BaseSettings ):

    gsi_url: str
    zzz_url: str
    hsr_url: str

    model_config = SettingsConfigDict( 
        extra = "allow",
    )
    
    @classmethod
    def from_yaml( cls, path: str ):
        
        file_path = Path( path )
        if not file_path.exists():
            raise FileNotFoundError( f"Yaml file not found: { file_path }" )
        
        content = {}
        with open( file_path, 'r', encoding='utf-8' ) as file:
            if file_path.suffix == '.yaml':
                content = yaml.safe_load( file )
                
            # print( f"Loaded config from { path }:\n{ content }" )
        
        return cls( **content )

@lru_cache()
def checkin_page_settings():
    return CheckInPageSettings.from_yaml( "./checkin_config.yaml" )

# print( checkin_page_settings().model_dump() )