import yaml
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from bot.storage.repositories import ConfigRepository

class HylabLoginSettings( BaseSettings ):

    name: str = "hylab_login_settings"

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
def hylab_login_settings( db ):
    
    config_repository = ConfigRepository( db )
    
    config = config_repository.get_config( "hylab_login_settings" )
    if config:
        return HylabLoginSettings( **config )
    
    config = HylabLoginSettings.from_yaml( "./login_settings.yaml" )
    config_repository.save_config( config.name, config.model_dump() )
    
    return config