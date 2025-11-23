import os
import shutil
import sys
from contextlib import contextmanager
from bot.jobs.check_in.settings import hylab_login_settings
from bot.storage.core.config import mongodb_settings
from bot.crawler import WebDriverFactory
from bot.notifier import DiscordNotifier
from bot.storage.core.dbs import MongoDB
from bot.storage.models.progress import DailyProgress
from bot.storage.repositories import CheckInProgressRepository
from bot.storage.service import ProgressService
from web.hyl.config import checkin_page_config
from web.hyl.models import CheckinResult
from web.hyl.pages import HyLPageFactory

@contextmanager
def db_connection():
    
    connection = MongoDB( mongodb_settings().URI )
    db = connection.database( mongodb_settings().DB_NAME )
    
    yield db
    
    connection.close()
    
    
def build_progress_payload( checkin_result: CheckinResult, 
                            last_progress: DailyProgress ):
    payload = { 
        "title": checkin_result.title,
        "url": checkin_result.page_url,
        "date": checkin_result.date,
        "progress": checkin_result.progress,
        "description": f"目前簽到: {last_progress.date}",
        "checkin_status": "",
    }
    
    if ( checkin_result.status == "success" and 
         last_progress.progress != checkin_result.progress ):
        
        payload[ "checkin_status" ] = "簽到成功"
        payload[ "description" ] = f"目前簽到: {checkin_result.date}"
        
    elif last_progress.progress == checkin_result.progress:
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
    
    headless = 1
    if headless:
        driver = WebDriverFactory.headless_chrome()
    else:
        driver = WebDriverFactory.chrome()
    
    with db_connection() as db:
        
        progress_repository = CheckInProgressRepository( db )
        progress_service = ProgressService( progress_repository )
        
        login_settings = hylab_login_settings( db ).model_dump()
        page_config = checkin_page_config( db ).model_dump()
        clear_screenshots( page_config )
        
        checkin_settings = login_settings | page_config
        # print( checkin_settings )
        
        for task_code in tasks:
            checkin_page = HyLPageFactory.create_page( task_code, driver, checkin_settings )
            
            checkin_page.open()
            checkin_page.login()
            checkin_result = checkin_page.daily_checkin()
            print( f"Check-in result:\n{ checkin_result }" )
            
            last_progress = progress_service.get_last_progress( task_code )
            print( f"Last check-in records:\n{ last_progress }" )
            
            progress_payload = build_progress_payload( checkin_result, last_progress )
            print( f"Check-in result payload:\n{ progress_payload }" )
            
            DiscordNotifier().notify_checkin_progress( progress_payload )
            
            if progress_payload[ "checkin_status" ] == "簽到成功":
                
                dp = DailyProgress.model_validate( progress_payload )
                progress_service.save_progress( dp )
    
    driver.quit()