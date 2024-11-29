from selenium import webdriver
from selenium.webdriver.common.by import By
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


opts = webdriver.ChromeOptions(  )
opts.timeouts = { 'implicit': 5000 }

driver = webdriver.Chrome( options = opts )
driver.implicitly_wait(10)

config = Config( "./config.yaml" )

driver.get( config.yaml[ "page_url" ] )
page_title = driver.find_element( By.XPATH, config.yaml[ "page_title" ][ "xpath" ] )
print( "page_title: " + page_title.text )

if ( not config.yaml[ "page_title" ][ "text" ] and page_title.text ):
    config.yaml[ "page_title" ][ "text" ] = page_title.text
    config.update()

target = driver.find_element( By.XPATH, config.yaml[ "target" ][ "xpath" ] )
print( "target_title: " + target.text )

if ( not config.yaml[ "target" ][ "text" ] == target.text ):
    print( "new episode!" )
    config.yaml[ "target" ][ "text" ] = target.text
    config.update()

driver.quit()

# python src/bot/crawler.py
# if __name__ == "__main__":