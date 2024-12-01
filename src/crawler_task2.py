import time
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bot.crawler import WebDriverFactory, Config

def add_item_to_local_storage( driver: Chrome ) -> None:
    key = "signin-guide-key"
    value = '{ "createdTime": 1732995969932, "cacheTime": 0, "data": true }'
    script = f"window.localStorage.setItem( '{ key }', '{ value }' );"
    
    driver.execute_script( script )
    
def add_cookies( driver: Chrome ):
    cookies = Config( "./task2_cookies.json" )
    for each in cookies.file:
        driver.add_cookie( each )

# python src/crawler_task2.py
if __name__ == "__main__":
    config = Config( "./task2_config.yaml" )
    driver = WebDriverFactory.chrome()
   
    driver.get( config.file[ "page_url" ] )
    
    # close pop-up window
    add_item_to_local_storage( driver )
    driver.refresh()
    
    # login
    login_icon = config.file[ "login_icon" ]
    login_element = WebDriverWait( driver, 3 ).until( EC.element_to_be_clickable( ( By.XPATH, login_icon[ "xpath" ] ) ) )
    login_element.click()
    
    add_cookies( driver )
    driver.refresh()
    time.sleep( 1 )

    # sign-in
    try:
        days = config.file[ "days" ]
        days_element = WebDriverWait( driver, 3 ).until( EC.element_to_be_clickable( ( By.XPATH, days[ "xpath" ] ) ) )
        days_text = days_element.text
        days_element.click()
        
        print( driver.title )
        print( days_text )
        
        if ( not config.file[ "page_title" ][ "text" ] ):
            config.file[ "page_title" ][ "text" ] = driver.title
    
        if ( not config.file[ "page_title" ][ "text" ] == days_text ):
            config.file[ "days" ][ "text" ] = days_text
    
        config.update()
    except TimeoutException:
        print( "已簽到" )
    except Exception as ex:
        print( ex )
    finally:
        driver.quit()