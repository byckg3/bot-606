import os
import shutil
import sys
from contextlib import contextmanager
from bot.config import mongodb_settings
from bot.crawler import WebDriverFactory
from bot.notifier import DiscordNotifier
from bot.storage.db import MongoDB
from bot.storage.repositories import CheckInProgressRepository
from bot.storage.service import ProgressService
from web.hyl.config import checkin_page_settings
from web.hyl.page import HyLPageFactory

@contextmanager
def progress_service():
    
    connection = MongoDB( mongodb_settings().URI )
    db = connection.database( mongodb_settings().DB_NAME )
    
    progress_repository = CheckInProgressRepository( db )
    progress_service = ProgressService( progress_repository )
    
    yield progress_service
    
    print( "\nTeardown CheckInProgressRepository for tests" )
    connection.close()
    
    
def build_progress_payload( checkin_result, last_progress = {} ):
    payload = { 
        "title": checkin_result[ "title" ],
        "url": checkin_result[ "page_url" ],
        "date": checkin_result[ "date" ],
        "progress": checkin_result[ "progress" ],
        "description": f"目前簽到: {last_progress.get( "date", "" )}",
        "checkin_status": "",
    }
    
    if ( checkin_result[ "status" ] == "success" and 
         last_progress.get( "progress", "" ) != checkin_result[ "progress" ] ):
        
        payload[ "checkin_status" ] = "簽到成功"
        payload[ "description" ] = f"目前簽到: {checkin_result[ "date" ]}"
        
    elif last_progress.get( "progress", "" ) == checkin_result[ "progress" ]:
        payload[ "checkin_status" ] = "已簽到"
        
    else:
        payload[ "checkin_status" ] = "簽到失敗"
    
    return payload


def clear_screenshots( config ):
    
    dir_name = config[ "screenshot_dir" ]

    if os.path.exists( dir_name ):
        shutil.rmtree( dir_name )

    os.makedirs( dir_name )

# set PYTHONPATH=%cd%\src
# python src\daily_checkin.py gsi zzz hsr
if __name__ == "__main__":
    
    tasks: list[ str ] = [ "gsi" ]
    if len( sys.argv ) >= 2:
        tasks = sys.argv[ 1: ]
    
    settings = checkin_page_settings().model_dump()
    clear_screenshots( settings )
    
    headless = 1
    if headless:
        driver = WebDriverFactory.headless_chrome()
    else:
        driver = WebDriverFactory.chrome()
    
    with progress_service() as storage_service:
        for task_name in tasks:
           
            checkin_page = HyLPageFactory.create_page( task_name, driver, settings )
            
            checkin_page.open()
            checkin_page.login()
            checkin_result = checkin_page.daliy_checkin()
            
            last_progress = storage_service.get_last_progress( task_name )
            # print( f"Last check-in records: { last_progress }" )
            progress_payload = build_progress_payload( checkin_result, last_progress )
            
            DiscordNotifier().notify_checkin_progress( progress_payload )
            
            if progress_payload[ "checkin_status" ] == "簽到成功":
                storage_service.save_progress(
                    { 
                        "title": progress_payload[ "title" ],
                        "progress": progress_payload[ "progress" ],
                        "metadata": { 
                            "task_name": task_name, 
                            "date": progress_payload[ "date" ],
                        }
                    } 
                )
    
    driver.quit()