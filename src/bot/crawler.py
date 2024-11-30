from selenium import webdriver
import yaml

class Config:
    file_path: str
    yaml: dict[ str, any ]
    
    def __init__( self, path: str = "./config.yaml" ):
        self.file_path = path
        with open( self.file_path, "r", encoding="utf-8" ) as file:
            self.yaml = yaml.safe_load( file )
            
    def set( self, key:str, value:str ):
        self.yaml[ key ] = value
        self.update()
        
    def update( self ):
        with open( self.file_path, "w", encoding="utf-8" ) as file:
            yaml.dump( self.yaml, file, allow_unicode = True )

class WebDriverFactory:
    
    @staticmethod
    def Chrome( isHeadless: bool = True ):
        opts = webdriver.ChromeOptions(  )
        opts.timeouts = { 'implicit': 5000 }
        
        opts.add_argument( "--no-sandbox" )
        opts.add_argument( "--disable-gpu" )
        if ( isHeadless ):
            opts.add_argument( "--headless" )
    
        driver = webdriver.Chrome( options = opts )
        driver.implicitly_wait( 10 )
        
        return driver