import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Self
from abc import ABC, abstractmethod
from web.hyl.component import HyLabHeader

class HyLCheckInPage( ABC ):
    
    header: HyLabHeader
    close_icon_locator: tuple[ By, str ]
    ith_days_locator: tuple[ By, str ]
    latest_days_locator : tuple[ By, str ]
    finish_locator : tuple[ By, str ]
    
    
    def __init__( self, webdriver: Chrome, config: dict[ str, any] ):
        self.driver = webdriver
        self.config = config
        self.current_progress = ""
        self.header = HyLabHeader( self.driver, self.config )
        
    def add_item_to_local_storage( self ) -> None:
        item: dict = self.config[ "ls_item" ]
        key = item[ "key" ]
        value = item[ "value" ]
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

    def daliy_checkin( self ) -> Self:
        try:
            ith_days_element = WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( self.ith_days_locator ) )
            self.current_progress = ith_days_element.text
            ith_days_element.click()
            
            WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( self.finish_locator ) )
            
        except TimeoutException:
            if ( not self.current_progress ):
                self.current_progress = WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( self.latest_days_locator ) ).text
            
        except Exception as ex:
            print( ex )
        
        return self
    
class GSICheckInPage( HyLCheckInPage ):
    close_icon_locator = ( By.XPATH, '//*[ contains( @class, "guide-close" ) ]' )
    ith_days_locator = (  By.XPATH, '//*[ contains( @class, "actived-day" ) ]/../*[ contains( @class, "item-day") ]' )
    latest_days_locator = (  By.XPATH, '( //*[ contains( @class, "has-signed" ) ])[ last() ]/*[ contains( @class, "item-day" ) ]' )
    finish_locator = ( By.XPATH, '//*[  contains( text(), "簽到成功" ) ]' )
    
    def __init__( self, webdriver: Chrome, config: dict[ str, any] ):
        super().__init__( webdriver, config )

class ZZZCheckInPage( HyLCheckInPage ):
    close_icon_locator = ( By.XPATH, '//*[ contains( @class, "dialog-close" ) ]' )
    ith_days_locator = (  By.XPATH, '//*[ contains( @style, "3b211daae47"  ) ]/*[  contains( @class, "no" ) ]' )
    latest_days_locator = (  By.XPATH, '( //*[ contains( @src, "d0ef8d6be" ) ] )[ last() ]/../*[ contains( @class, "no" ) ]' )
    finish_locator = ( By.XPATH, '//*[ contains( text(), "簽到成功" ) ]' )
    
    def __init__( self, webdriver: Chrome, config: dict[ str, any] ):
        super().__init__( webdriver, config )