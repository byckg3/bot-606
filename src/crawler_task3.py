import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Self
from bot.crawler import WebDriverFactory, Config

class CheckInPage:
    
    before_login_locator = ( By.XPATH, '//*[ contains( @class, "avatar-icon" ) and contains( @src, "image/png" ) ]' )
    after_login_locator = ( By.XPATH, '//*[ contains( @class, "avatar-icon" ) and contains( @src, "avatar" ) ]' )
    
    close_icon_locator = ( By.XPATH, '//*[ contains( @class, "dialog-close" ) ]' )
    ith_days_locator = (  By.XPATH, '//*[ contains( @style, "3b211daae47"  ) ]/*[  contains( @class, "no" ) ]' )
    latest_days_locator = (  By.XPATH, '( //*[ contains( @src, "d0ef8d6be" ) ] )[ last() ]/../*[ contains( @class, "no" ) ]' )
    finish_locator = ( By.XPATH, '//*[ contains( text(), "簽到成功" ) ]' )
    
    def __init__( self, webdriver: Chrome, config: dict[ str, any] ):
        self.driver = webdriver
        self.config = config
        self.current_progress = ""
    
    def add_item_to_local_storage( self ) -> None:
        item: dict = self.config[ "ls_item" ]
        key = item[ "key" ]
        value = item[ "value" ]
        script = f"window.localStorage.setItem( '{ key }', '{ value }' );"
        
        self.driver.execute_script( script )
        
    def add_cookies_for_login( self ) -> None:
        cookies: list = self.config[ "cookies" ]
        for each in cookies:
            self.driver.add_cookie( each )
            
    def close_popup_window( self ) -> Self:
        try:
            self.add_item_to_local_storage()
            self.driver.refresh()
        except Exception as ex:
            print( ex )
            
        return self
    
    def login( self ) -> Self:
        self.close_popup_window()
        try:
            WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( CheckInPage.before_login_locator ) ).click()
            self.add_cookies_for_login()
            self.driver.refresh()
            
            time.sleep( 2 )
            WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( CheckInPage.after_login_locator ) )
        except Exception as ex:
            print( ex )
       
        return self
    
    def daliy_checkin( self ) -> Self:
        try:
            ith_days_element = WebDriverWait( self.driver, 3 ).until( EC.element_to_be_clickable( CheckInPage.ith_days_locator ) )
            self.current_progress = ith_days_element.text
            ith_days_element.click()
            
            WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( CheckInPage.finish_locator ) )
            
        except TimeoutException:
            if ( not self.current_progress ):
                self.current_progress = WebDriverWait( self.driver, 3 ).until( EC.visibility_of_element_located( CheckInPage.latest_days_locator ) ).text
            
        except Exception as ex:
            print( ex )
        
        return self
        
# python src/crawler_task3.py
if __name__ == "__main__":
    config = Config( "./task3_config.yaml" )
    
    driver = WebDriverFactory.chrome()
    driver.get( config.content[ "page_url" ] )
    
    checkin_page = CheckInPage( driver, config.content )
    checkin_page.login()
    checkin_page.daliy_checkin()
    
    print( driver.title )
    output = Config( "./task3_info.yaml" )
    if ( not output.content[ "title" ] ):
        output.content[ "title" ] = driver.title
        
    print( f" { checkin_page.current_progress }", end = " " )
    if ( not output.content[ "progress" ] == checkin_page.current_progress ):
        output.content[ "progress" ] = checkin_page.current_progress
    else:
        print( "已簽到" )
        
    output.update()
    
    driver.quit()