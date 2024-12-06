import sys
from bot.crawler import Config, WebDriverFactory
from web.hyl.page import HyLPageFactory

def hylab_checkin( task_name: str ):
    config = Config( "./checkin_config.yaml" )
    
    driver = WebDriverFactory.chrome()
    driver.get( config.content[ task_name + "_url" ] )
    
    checkin_page = HyLPageFactory.create_page( task_name, driver, config.content )
    checkin_page.login()
    result = checkin_page.daliy_checkin()
    
    save_progress( task_name, result )
    
    driver.quit()
    
def save_progress( task_name: str, task: dict[ str, any ] ):
    
    print( task[ "title" ] )
    output = Config( "./checkin_info.yaml" )
    
    if ( not output.content[ task_name ][ "title" ] ):
        output.content[ task_name ][ "title" ] = task[ "title" ]
        
    print( f" { task[ "progress" ] }", end = " " )
    if ( task[ "state" ] == "success" and not output.content[ task_name ][ "progress" ] == task[ "progress" ] ):
        output.content[ task_name ][ "progress" ] = task[ "progress" ]
        output.content[ task_name ][ "date" ] = task[ "date" ]
        print( "簽到成功" )
    elif output.content[ task_name ][ "progress" ] == task[ "progress" ]:
        print( "已簽到" )
    else:
        print( "簽到失敗" )
        
    print( f"目前簽到: { output.content[ task_name ][ "date" ] }" )
    output.update()


# python src/checkin.py gsi
# python src/checkin.py gsi zzz 
# python src/checkin.py gsi zzz hsr
if __name__ == "__main__":
    targets = [ "gsi" ]
    if len( sys.argv ) >= 2:
        targets = sys.argv[ 1: ]
    
    for target in targets:
        hylab_checkin( target )