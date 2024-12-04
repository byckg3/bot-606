import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Self

class HyLabHeader:
    
    before_login_locator = ( By.XPATH, '//*[ contains( @class, "avatar-icon" ) and contains( @src, "image/png" ) ]' )
    after_login_locator = ( By.XPATH, '//*[ contains( @class, "avatar-icon" ) and contains( @src, "avatar" ) ]' )
    
    def __init__( self, webdriver: Chrome, config: dict[ str, any] ):
        self.driver = webdriver
        self.config = config
    
    def add_cookies_for_signin( self ) -> None:
        cookies: list = self.config[ "cookies" ]
        for each in cookies:
            self.driver.add_cookie( each )
            
    def signin( self ) -> Self:
        try:
            WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( HyLabHeader.before_login_locator ) ).click()
            self.add_cookies_for_signin()
            
            self.driver.refresh()
            time.sleep( 2 )
        except TimeoutException as ex:
            print( ex )
        
        WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( HyLabHeader.after_login_locator ) )
        
        return self