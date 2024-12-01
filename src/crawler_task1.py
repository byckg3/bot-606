from selenium.webdriver.common.by import By
from bot.crawler import WebDriverFactory, Config

# python src/crawler_task1.py
if __name__ == "__main__":
    driver = WebDriverFactory.headless_chrome()
    config = Config( "./task1_config.yaml" )

    driver.get( config.file[ "page_url" ] )
    page_title = driver.find_element( By.XPATH, config.file[ "page_title" ][ "xpath" ] )
    print( "title: " + page_title.text )

    if ( not config.file[ "page_title" ][ "text" ] ):
        config.file[ "page_title" ][ "text" ] = page_title.text
        config.update()

    target = driver.find_element( By.XPATH, config.file[ "target" ][ "xpath" ] )
    print( "latest: " + target.text )

    if ( not config.file[ "target" ][ "text" ] == target.text ):
        print( "new episode!! \n" + config.file[ "page_url" ] )
        config.file[ "target" ][ "text" ] = target.text
        config.update()

    driver.quit()