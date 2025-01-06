import sys
from bot.crawler import Config, WebDriverFactory
from bot.notifier import DiscordNotifier
from web.hyl.page import HyLPageFactory

def hylab_checkin( task_name: str ):
    config = Config( "./checkin_config.yaml" )
    
    driver = WebDriverFactory.headless_chrome()
    driver.get( config.content[ task_name + "_url" ] )
    
    checkin_page = HyLPageFactory.create_page( task_name, driver, config.content )
    checkin_page.login()
    result = checkin_page.daliy_checkin()
    
    msg = save_progress( task_name, result )
    msg[ "url" ] = config.content[ task_name + "_url" ]
    
    DiscordNotifier().notify( **msg )
    
    driver.quit()
    
def save_progress( task_name: str, task: dict[ str, any ] ):
    
    saved_file = Config( "./checkin_info.yaml" )
    message = { 
        "title": "",
        "state": "",
        "progress": "",
        "description": "",
        "url": ""
    }
    
    message[ "title" ] = task[ 'title' ]
    if ( not saved_file.content[ task_name ][ "title" ] ):
        saved_file.content[ task_name ][ "title" ] = task[ "title" ]
        
    message[ "progress" ] = task[ 'progress' ]
    if ( task[ "state" ] == "success" and not saved_file.content[ task_name ][ "progress" ] == task[ "progress" ] ):
        saved_file.content[ task_name ][ "progress" ] = task[ "progress" ]
        saved_file.content[ task_name ][ "date" ] = task[ "date" ]
        message[ "state" ] = "簽到成功"
    elif saved_file.content[ task_name ][ "progress" ] == task[ "progress" ]:
        message[ "state" ] = "已簽到"
    else:
        message[ "state" ] = "簽到失敗"
        
    message[ "description" ] = f"目前簽到: { saved_file.content[ task_name ][ 'date' ] }"
    
    saved_file.update()
    print( f"{ message[ "title" ] }\n{ message[ "progress" ] } { message[ "state" ] }\n{ message[ "description" ] }" )
    
    return message

# python src/checkin.py gsi
# python src/checkin.py gsi zzz 
# python src/checkin.py gsi zzz hsr
if __name__ == "__main__":
    targets = [ "gsi" ]
    if len( sys.argv ) >= 2:
        targets = sys.argv[ 1: ]
    
    for target in targets:
        hylab_checkin( target )