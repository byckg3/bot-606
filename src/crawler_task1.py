from selenium.webdriver.common.by import By
from bot.crawler import WebDriverFactory, Config

# python src/crawler_task1.py
if __name__ == "__main__":
    driver = WebDriverFactory.Chrome()
    config = Config( "./task1_config.yaml" )

    driver.get( config.yaml[ "page_url" ] )
    page_title = driver.find_element( By.XPATH, config.yaml[ "page_title" ][ "xpath" ] )
    print( "title: " + page_title.text )

    if ( not config.yaml[ "page_title" ][ "text" ] ):
        config.yaml[ "page_title" ][ "text" ] = page_title.text
        config.update()

    target = driver.find_element( By.XPATH, config.yaml[ "target" ][ "xpath" ] )
    print( "latest: " + target.text )

    if ( not config.yaml[ "target" ][ "text" ] == target.text ):
        print( "new episode!! \n" + config.yaml[ "page_url" ] )
        config.yaml[ "target" ][ "text" ] = target.text
        config.update()

    driver.quit()