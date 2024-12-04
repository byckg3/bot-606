from bot.crawler import WebDriverFactory, Config
from web.hyl.page import ZZZCheckInPage

# python src/crawler_task3.py
if __name__ == "__main__":
    config = Config( "./task3_config.yaml" )
    
    driver = WebDriverFactory.chrome()
    driver.get( config.content[ "page_url" ] )
    
    checkin_page = ZZZCheckInPage( driver, config.content )
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