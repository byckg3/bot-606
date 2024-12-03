from selenium.webdriver.common.by import By
from bot.crawler import WebDriverFactory, Config

# python src/crawler_task1.py
if __name__ == "__main__":
    driver = WebDriverFactory.headless_chrome()
    config = Config( "./task1_config.yaml" )

    driver.get( config.content[ "page_url" ] )
    page_title = driver.find_element( By.XPATH, config.content[ "page_title" ][ "xpath" ] )
    print( "title: " + page_title.text )

    if ( not config.content[ "page_title" ][ "text" ] ):
        config.content[ "page_title" ][ "text" ] = page_title.text
        config.update()

    target = driver.find_element( By.XPATH, config.content[ "target" ][ "xpath" ] )
    print( "latest: " + target.text )

    if ( not config.content[ "target" ][ "text" ] == target.text ):
        print( "new episode!! \n" + config.content[ "page_url" ] )
        config.content[ "target" ][ "text" ] = target.text
        config.update()

    driver.quit()