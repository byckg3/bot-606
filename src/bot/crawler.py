from selenium import webdriver
from pathlib import Path
import yaml
import json

class Config:
    file_path: Path
    file: dict[ str, any ] | list
    
    def __init__( self, path: str  ):
        self.file_path = Path( path )
        
        with open( self.file_path, 'r', encoding='utf-8') as file:
            if self.file_path.suffix == '.yaml':
                self.file = yaml.safe_load( file )
            elif self.file_path.suffix == '.json':
                self.file = json.load( file )
     
    def update( self ):
        with open( self.file_path, "w", encoding="utf-8" ) as file:
            yaml.dump( self.file, file, allow_unicode = True )

class WebDriverFactory:
    
    @staticmethod
    def chrome( isHeadless: bool = False ):
        
        opts = webdriver.ChromeOptions(  )
        opts.add_argument( "--disable-popup-blocking" )
        opts.add_argument( "--no-sandbox" )
        opts.add_argument( "--lang=zh-TW" )
        if ( isHeadless ):
            opts.add_argument( "--headless" )
            # opts.add_argument( "--disable-gpu" )
            # opts.add_argument( "--disable-software-rasterizer" )
            
        preferences = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream": 2
        }
        opts.add_experimental_option( "prefs", preferences )
    
        driver = webdriver.Chrome( options = opts )
        driver.implicitly_wait( 10 )
        
        return driver
    
    @staticmethod
    def headless_chrome():
        return WebDriverFactory.chrome( True )

# python src/bot/crawler.py
if __name__ == "__main__":
    cfg = Config( "./task2_cookies.json" )
    print( cfg.json[ 0 ][ "name" ] )