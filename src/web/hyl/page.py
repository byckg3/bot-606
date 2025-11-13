import time
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Any, Self
from abc import ABC, abstractmethod
from web.hyl.component import HyLabHeader

class HyLCheckInPage( ABC ):
    
    close_icon_locator: tuple[ str, str ] = ( By.XPATH, '//*[ contains( @class, "close" ) ]' )
    finish_locator : tuple[ str, str ] = ( By.XPATH, '//*[ contains( text(), "簽到成功" ) ]' )
    
    def __init__( self, webdriver: Chrome, config: dict[ str, Any] ):
        self.driver = webdriver
        self.config = config
        self.current_progress = ""
        self.header = HyLabHeader( self.driver, self.config )
        
    @property
    @abstractmethod
    def ith_days_locator( self ) -> tuple[ str, str ]:
        pass
    
    @property
    @abstractmethod
    def latest_days_locator( self ) -> tuple[ str, str ]:
        pass
        
    def add_item_to_local_storage( self ) -> None:
        item: dict = self.config[ "ls_item" ]
        key, value = item[ "key" ], item[ "value" ]  
        script = f"window.localStorage.setItem( '{ key }', '{ value }' );"
        
        self.driver.execute_script( script )
            
    def close_popup_window( self ) -> Self:
        self.add_item_to_local_storage()
        
        self.driver.refresh()
        time.sleep( 1 )
        
        return self
    
    def login( self ) -> Self:
        try:
            self.close_popup_window()
            self.header.signin()
        except Exception as ex:
            print( ex )
       
        return self

    def daliy_checkin( self ) -> dict[ str, str]:
        
        log = { "title": None, "state": "failed", "date": None }
        log[ "title" ] = self.driver.title
        try:
            ith_days_element = WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( self.ith_days_locator ) )
            log[ "progress" ] = ith_days_element.text
            
            ith_days_element.click()
            WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( self.finish_locator ) )
            
            log[ "state" ] = "success"
            log[ "date" ] = date.today()

        except TimeoutException:
            if log[ "state" ] == "failed":
                log[ "progress" ] = WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( self.latest_days_locator ) ).text

        except Exception as ex:
            self.save_screenshot()
            print( ex )
        
        return log
    
    def save_screenshot( self ):
        timestamp = time.strftime( "%y%m%d_%H%M%S" )
        self.driver.save_screenshot( self.config[ "screenshot_dir" ] + f"/{timestamp}.png" )
    
class GSICheckInPage( HyLCheckInPage ):
    
    ith_days_locator: tuple[ str, str ] = (  By.XPATH, '//*[ contains( @class, "actived-day" ) ]/../*[ contains( @class, "item-day") ]' )
    latest_days_locator: tuple[ str, str ] = (  By.XPATH, '( //*[ contains( @class, "has-signed" ) ])[ last() ]/*[ contains( @class, "item-day" ) ]' )
    
    
    def __init__( self, webdriver: Chrome, config: dict[ str, Any] ):
        super().__init__( webdriver, config )

class ZZZCheckInPage( HyLCheckInPage ):
    
    ith_days_locator: tuple[ str, str ] = (  By.XPATH, '//*[ contains( @style, "3b211daae47"  ) ]/*[  contains( @class, "no" ) ]' )
    latest_days_locator: tuple[ str, str ] = (  By.XPATH, '( //*[ contains( @src, "d0ef8d6be" ) ] )[ last() ]/../*[ contains( @class, "no" ) ]' )
   
    def __init__( self, webdriver: Chrome, config: dict[ str, Any] ):
        super().__init__( webdriver, config )
        
class HSRCheckInPage( HyLCheckInPage ):
   
    ith_days_locator: tuple[ str, str ] = (  By.XPATH, '//*[ contains( @style, "5ccbbab8f"  ) ]/*[  contains( @class, "no" ) ]' )
    latest_days_locator: tuple[ str, str ] = (  By.XPATH, '( //*[ contains( @class, "received" ) ] )[ last() ]/preceding-sibling::*[ contains( @class, "no" ) ]' )
    
    
    def __init__( self, webdriver: Chrome, config: dict[ str, Any] ):
        super().__init__( webdriver, config )
        
class HyLPageFactory:
    
    @staticmethod
    def create_page( page_name: str, webdriver: Chrome, config: dict[ str, Any ] ) -> HyLCheckInPage:
        
        match page_name:
            case "gsi":
                return GSICheckInPage( webdriver, config )
            case "zzz":
                return ZZZCheckInPage( webdriver, config )
            case "hsr":
                return HSRCheckInPage( webdriver, config )
            case _:
                raise ValueError( f"Unknown page name: { page_name }" )