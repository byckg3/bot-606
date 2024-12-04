import sys
from bot.crawler import Config, WebDriverFactory
from web.hyl.page import HyLPageFactory

def hylab_checkin( task_name: str ):
    config = Config( "./checkin_config.yaml" )
    
    driver = WebDriverFactory.chrome()
    driver.get( config.content[ task_name + "_url" ] )
    
    checkin_page = HyLPageFactory.create_page( task_name, driver, config.content )
    checkin_page.login()
    checkin_page.daliy_checkin()
    
    print( driver.title )
    output = Config( "./checkin_info.yaml" )
    if ( not output.content[ task_name ][ "title" ] ):
        output.content[ task_name ][ "title" ] = driver.title
        
    print( f" { checkin_page.current_progress }", end = " " )
    if ( not output.content[ task_name ][ "progress" ] == checkin_page.current_progress ):
        output.content[ task_name ][ "progress" ] = checkin_page.current_progress
    else:
        print( "已簽到" )
        
    output.update()
    
    driver.quit()


# python src/checkin.py gsi
# python src/checkin.py zzz
# python src/checkin.py hsr
if __name__ == "__main__":
    target_name = sys.argv[1] if sys.argv[1] else "gsi"
    hylab_checkin( target_name )