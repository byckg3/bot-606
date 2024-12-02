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
    close_icon_locator = ( By.XPATH, '//*[ contains( @class, "guide-close" ) ]' )
    ith_days_locator = (  By.XPATH, '//*[ contains( @class, "actived-day" ) ]/../*[ contains( @class, "item-day") ]' )
    latest_days_locator = (  By.XPATH, '( //*[ contains( @class, "has-signed" ) ])[ last() ]/*[ contains( @class, "item-day" ) ]' )
    finish_locator = ( By.XPATH, '//*[  contains( text(), "簽到成功" ) ]' )
    
    def __init__( self, webdriver ):
        self.driver = webdriver
        self.current_progress = ""
        self.cookie_file_path = "./task2_cookies.json"
    
    def add_item_to_local_storage( self ) -> None:
        key = "signin-guide-key"
        value = '{ "createdTime": 1732995969932, "cacheTime": 0, "data": true }'
        script = f"window.localStorage.setItem( '{ key }', '{ value }' );"
        
        self.driver.execute_script( script )
        
    def add_cookies_for_login( self ) -> None:
        cookies = Config( self.cookie_file_path )
        for each in cookies.file:
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
            
            time.sleep( 1 )
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

# python src/crawler_task2.py
if __name__ == "__main__":
    config = Config( "./task2_config.yaml" )
    
    driver = WebDriverFactory.headless_chrome()
    driver.get( config.file[ "page_url" ] )
    
    checkin_page = CheckInPage( driver )
    checkin_page.login()
    checkin_page.daliy_checkin()
    
    print( driver.title )
    if ( not config.file[ "page_title" ] ):
        config.file[ "page_title" ] = driver.title
        
    print( f" { checkin_page.current_progress }", end = " " )
    if ( not config.file[ "progress" ] == checkin_page.current_progress ):
        config.file[ "progress" ] = checkin_page.current_progress
    else:
        print( "已簽到" )
        
    config.update()
    
    driver.quit()